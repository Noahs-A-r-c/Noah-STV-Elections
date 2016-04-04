import wx
import wx.lib.delayedresult
import time
import logging
from ElectionUIRacePanel import ElectionUIRacePanel
from ElectionRace import ElectionRace
from ElectionRaceRound import ElectionRaceRound
from ElectionApplicationAbout import ElectionApplicationAbout


class ElectionMainUI(wx.Frame):

    def __init__(self, parent, election):
        wx.Frame.__init__(self, parent, size=(900, 680))

        self.logger = logging.getLogger("application.ui.main")

        self.election = election

        self._election_states = {
            ElectionRace.COMPLETE: "Complete",
            ElectionRace.TABULATING: "Tabulating",
            ElectionRace.ADDING: "Adding"
        }

        self._election_round_states = {
            ElectionRaceRound.COMPLETE: "Complete",
            ElectionRaceRound.INCOMPLETE: "Incomplete"
        }

        # Menu variables.
        self.menu = None
        self.menu_file = None
        self.menu_file_new = None
        self.menu_help = None
        self.menu_help_about = None

        # Display select controls.
        self.panel_display_select = None
        self.label_race = None
        self.label_round = None
        self.label_speed = None
        self.combo_box_race = None
        self.combo_box_round = None
        self.slider_display_speed = None

        # Display grid.
        self.panel_display_grid = None
        self.grid_display = None

        # Display race controls.
        self.panel_display_control = None
        self.label_quota = None
        self.button_complete_round = None
        self.button_complete_race = None

        # Display sizer.
        self.sizer = None
        self.sizer_display_select = None
        self.sizer_display_grid = None
        self.sizer_display_control = None

        # Race combo-box option text to object relationship.
        self.combo_box_race_object = {}

        # Round combo-box option text to object relationship.
        self.combo_box_round_object = {}

        # Current race and round.
        self._current_race = None
        self._current_round = None

        # Currently running a race/round.
        self._current_running = False

        self.show_ui()
        self.Centre()
        self.Show()
        self.logger.info("Main application user interface displayed.")

    def show_ui(self):
        self.logger.info("Launching main application user interface.")

        # Status Bar
        self.CreateStatusBar()

        # Menu
        self.menu = wx.MenuBar()

        # File Menu
        self.logger.debug("Creating file menu.")
        self.menu_file = wx.Menu()

        # File Menu > New Election
        self.menu_file_new = self.menu_file.Append(wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.show_new, self.menu_file_new)

        self.menu.Append(self.menu_file, "&File")

        # Help Menu
        self.logger.debug("Creating help menu.")
        self.menu_help = wx.Menu()

        # Help Menu > About
        self.menu_help_about = self.menu_help.Append(wx.ID_ABOUT, "&About UCSB AS Election Tabulator")
        self.Bind(wx.EVT_MENU, self.show_about, self.menu_help_about)

        self.menu.Append(self.menu_help, "&Help")

        self.SetMenuBar(self.menu)

        self.panel_display_select = wx.Panel(self, wx.ID_ANY)
        self.label_race = wx.StaticText(self.panel_display_select, wx.ID_ANY, "Race")
        self.label_round = wx.StaticText(self.panel_display_select, wx.ID_ANY, "Round")
        self.label_speed = wx.StaticText(self.panel_display_select, wx.ID_ANY, "Display Speed")
        self.combo_box_race = wx.ComboBox(self.panel_display_select, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.combo_box_round = wx.ComboBox(self.panel_display_select, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.panel_display_select.Bind(wx.EVT_COMBOBOX, self.ui_combobox_event)
        self.slider_display_speed = wx.Slider(self.panel_display_select, wx.ID_ANY, 0, 0, 100)
        self.slider_display_speed.SetValue(90)

        self.panel_display_grid = wx.Panel(self, wx.ID_ANY)
        self.grid_display = ElectionUIRacePanel(self.panel_display_grid)

        self.panel_display_control = wx.Panel(self, wx.ID_ANY)
        self.label_quota = wx.StaticText(self.panel_display_control, wx.ID_ANY, "")
        self.button_complete_round = wx.Button(self.panel_display_control, wx.ID_ANY, "Complete Round")
        self.panel_display_control.Bind(wx.EVT_BUTTON, self.ui_complete_round, self.button_complete_round)
        self.button_complete_race = wx.Button(self.panel_display_control, wx.ID_ANY, "Complete Race")
        self.panel_display_control.Bind(wx.EVT_BUTTON, self.ui_complete_race, self.button_complete_race)

        self.sizer_display_select = wx.FlexGridSizer(2, 6, 0, 0)
        self.sizer_display_select.AddGrowableCol(3)
        self.panel_display_select.SetSizer(self.sizer_display_select)

        self.sizer_display_select.Add((20, 1), 0, 0, 0)
        self.sizer_display_select.Add(self.label_race, 0, 0, 0)
        self.sizer_display_select.Add(self.label_round, 0, 0, 0)
        self.sizer_display_select.Add((20, 20), 0, wx.EXPAND, 0)
        self.sizer_display_select.Add(self.label_speed, 0, 0, 0)
        self.sizer_display_select.Add((20, 1), 0, 0, 0)
        self.sizer_display_select.Add((20, 1), 0, 0, 0)
        self.sizer_display_select.Add(self.combo_box_race, 0, wx.BOTTOM | wx.RIGHT, 10)
        self.sizer_display_select.Add(self.combo_box_round, 0, wx.BOTTOM, 10)
        self.sizer_display_select.Add((20, 20), 0, wx.EXPAND, 0)
        self.sizer_display_select.Add(self.slider_display_speed, 0, wx.BOTTOM | wx.EXPAND, 5)
        self.sizer_display_select.Add((20, 1), 0, 0, 0)

        self.sizer_display_grid = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_display_grid.SetSizer(self.sizer_display_grid)

        self.sizer_display_grid.Add((20, 1), 0, 0, 0)
        self.sizer_display_grid.Add(self.grid_display, 1, wx.ALL | wx.EXPAND, 0)
        self.sizer_display_grid.Add((20, 1), 0, 0, 0)

        self.sizer_display_control = wx.FlexGridSizer(1, 6, 0, 0)
        self.sizer_display_control.AddGrowableRow(0)
        self.sizer_display_control.AddGrowableCol(2)
        self.panel_display_control.SetSizer(self.sizer_display_control)

        self.sizer_display_control.Add((20, 1), 0, 0, 0)
        self.sizer_display_control.Add(self.label_quota, 0, wx.TOP | wx.EXPAND, 5)
        self.sizer_display_control.Add((1, 1), 0, wx.EXPAND, 0)
        self.sizer_display_control.Add(self.button_complete_round, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 10)
        self.sizer_display_control.Add(self.button_complete_race, 0, wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.TOP, 10)
        self.sizer_display_control.Add((20, 1), 0, wx.EXPAND, 0)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.sizer.Add((1, 10), 0, 0, 0)
        self.sizer.Add(self.panel_display_select, 0, wx.EXPAND, 0)
        self.sizer.Add(self.panel_display_grid, 1, wx.EXPAND, 0)
        self.sizer.Add(self.panel_display_control, 0, wx.EXPAND, 0)
        self.sizer.Add((1, 5), 0, 0, 0)
        self.sizer.SetSizeHints(self)

        self.SetSize((750, 500))
        self.SetMinSize((750, 500))
        self.Layout()

        self.SetTitle("UCSB AS Election Tabulator")

        # Setup the UI state.
        combo_box_text = []

        election_races = self.election.get_race_all()
        if "display_order" in election_races[0].extended_data():
            election_races.sort(key=lambda election_race: election_race.extended_data()["display_order"])
        else:
            election_races.sort(key=lambda election_race: election_race.position())

        for race in election_races:
            # Add the race to possible races.
            self.combo_box_race_object[race.position()] = race
            combo_box_text.append(race.position())

        self.combo_box_race.SetItems(combo_box_text)
        self.change_race(election_races[0])
        self.combo_box_race.SetSelection(self.combo_box_race.FindString(self._current_race.position()))

        if "default_speed" in self.election.configuration()["general"]:
            self.logger.debug("Default tabulation speed set at `%d`.", self.election.configuration()["general"]["default_speed"])
            self.slider_display_speed.SetValue(self.election.configuration()["general"]["default_speed"])

    def show_about(self, event):
        ElectionApplicationAbout(self)

    def show_new(self, event):
        if wx.MessageDialog(self, "There is currently an election open. Would you like to close this election?", caption="Confirm Close", style=wx.YES_NO | wx.NO_DEFAULT | wx.CENTRE).ShowModal() == wx.ID_YES:
            self.Close(True)
            from ElectionNewUI import ElectionNewUI
            application_new_ui = ElectionNewUI(None)
            application_new_ui.ShowModal()
            application_new_ui.Destroy()

    def ui_combobox_event(self, event):
        if event.GetEventObject() is self.combo_box_race:
            self.change_race(self.combo_box_race_object[self.combo_box_race.GetStringSelection()])
        elif event.GetEventObject() is self.combo_box_round:
            selection_text = self.combo_box_round.GetStringSelection()
            if selection_text == "Latest Round":
                self.change_round(self._current_race.get_round_latest())
            else:
                self.change_round(self.combo_box_round_object[selection_text])
        button_state = self._current_round.parent().state() != ElectionRace.COMPLETE
        self.button_complete_race.Enable(button_state)
        self.button_complete_round.Enable(button_state)
        self.button_complete_round.SetFocus()

    def ui_complete_round(self, event):
        self.ui_disable_all()

        # Complete the current race.
        wx.lib.delayedresult.startWorker(self.ui_complete_action_done, self.complete_current_round)

    def ui_complete_race(self, event):
        self.ui_disable_all()

        # Complete the current round.
        wx.lib.delayedresult.startWorker(self.ui_complete_action_done, self.complete_current_race)

    def ui_disable_all(self):
        # Disable the complete current round/race button
        # and also disable the race change combo box.
        self.button_complete_race.Enable(False)
        self.button_complete_round.Enable(False)
        self.combo_box_race.Enable(False)
        self.combo_box_round.Enable(False)
        self.menu_file_new.Enable(False)

    def ui_complete_action_done(self, result):
        self.combo_box_race.Enable(True)
        self.combo_box_round.Enable(True)
        self.menu_file_new.Enable(True)
        if self._current_round.parent().state() != ElectionRace.COMPLETE:
            self.button_complete_race.Enable(True)
            self.button_complete_round.Enable(True)

    def ui_update_statusbar(self):
        if self._current_race is None or self._current_round is None:
            return

        self.SetStatusText("Race: " + self._election_states[self._current_race.state()] + " | Round: " + self._election_round_states[self._current_round.state()])

    def change_race(self, election_race):
        if self._current_race is election_race:
            return

        self._current_race = election_race
        self.ui_update_rounds(False)
        self.ui_update_statusbar()
        self.change_round(election_race.get_round_latest())
        self.label_quota.SetLabel("Race: " + election_race.position() + "\nRace Winning Quota: " + str(election_race.droop_quota()))

    def change_round(self, election_round):
        self._current_round = election_round
        self.grid_display.set_round(election_round)
        self.ui_update_statusbar()

    def ui_update_rounds(self, preserve_selection=True):
        self.combo_box_round_object = {}
        combo_box_text = []
        current_selection = "Latest Round"

        for election_round in self._current_race.rounds():
            self.combo_box_round_object["Round " + str(election_round.round())] = election_round
            combo_box_text.append("Round " + str(election_round.round()))

        combo_box_text.append("Latest Round")

        if preserve_selection and self.combo_box_round.GetStringSelection():
            current_selection = self.combo_box_round.GetStringSelection()

        self.combo_box_round.SetItems(combo_box_text)

        current_selection_position = self.combo_box_round.FindString(current_selection)
        if current_selection_position is not wx.NOT_FOUND:
            self.combo_box_round.SetSelection(current_selection_position)

    def complete_current_race(self):
        while self._current_race.state() != ElectionRace.COMPLETE:
            self.complete_current_round()
            wx.Yield()

    def complete_current_round(self):
        # Jump to latest round.
        self.change_round(self._current_race.get_round_latest())
        self.combo_box_round.SetSelection(self.combo_box_round.FindString("Latest Round"))

        while self._current_round.state() != ElectionRaceRound.COMPLETE:
            self.ui_update_statusbar()
            self._current_round.parent().run()
            self.grid_display.update()
            time.sleep((self.slider_display_speed.GetMax()+1 - self.slider_display_speed.GetValue())*0.0001)
            wx.Yield()

        self.ui_update_statusbar()

        self.grid_display.update()
        wx.Yield()
        self.ui_update_rounds()
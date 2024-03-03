UCDNOTES.md
Noah Nguyen ASUCD IT 8/2/2023

Debugging Notes:
- UC_STV has built in logs under UC_STV/logs/ that will help if your ballot does not run
- Parser
	- the configuration.json file must be in a directory with the /parser files as our example is
	- all candidates in the Clean Voting results must be in the format "Candidate - Party". The hyphen is necessary for the parser.

File locations:
- Parser JSON: UC_STV/qualtrics/parser/configuration.json
- Clean Votes CSV: UC_STV/qualtrics/results/"Example Voting Prototype Clean.csv"

Changes:
- I've commented out the EndModal() function in UC_STV/interfaces/gui/WindowNew.py on line 158 as it caused the elections software to close prematurely on my Windows 11 machine.

Working with Qualtrics:
- Clean ballots must be in the format as the example
- The Valid Voter list must be changed to a csv before being added
	- add the valid voter list into the second authenticator in each qualtrics survey (petition sign up, petition, voting). This is after CAS

The Voting Ballot
- Make sure that the order of responses in the questions are randomized! Default order being the same for every ballot for every candidate would give some candidates unfair advantages.
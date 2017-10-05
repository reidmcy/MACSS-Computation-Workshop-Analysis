import utils
import sys
import argparse

workshopOrgName = 'uchicago-computation-workshop'

def parseArgs():
    parser = argparse.ArgumentParser(description='Displays question likes for workshop talks')
    parser.add_argument('speaker', nargs='?', default=None, help='the speaker\'s name (or at least an unique substring)')
    return parser.parse_args()

def askForSpeaker(repos):
    while True:
        print("The avaiable speakers are:")
        for i, r in enumerate(repos):
            print("{}) {}".format(i + 1, r['name']))
        selection = input("Select the number of the speaker: ")
        try:
            s = int(selection) - 1
            targetRepo = repos[s]
        except:
            print("That is not a valid selection")
        else:
            return targetRepo


def main():
    args = parseArgs()
    repos = utils.getRepos()
    if args.speaker is None:
        targetRepo = askForSpeaker(repos)
    else:
        selection = [r for r in repos if args.speaker in r['name']]
        if len(selection) == 0:
            print("{} was not found in any of the speaker's names")
            targetRepo = askForSpeaker(repos)
        elif len(selection) == 1:
            targetRepo = selection[0]
        else:
            print("{} was found in mutiple speaker's names")
            targetRepo = askForSpeaker(selection)
    utils.getIssues(targetRepo)
if __name__ == '__main__':
    main()

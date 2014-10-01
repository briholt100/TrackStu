import time
import os.path


def list_tocsv(list, filename):
    import csv
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(list)



def to_csv(players):
    stat_file = [['player','category', 'attribute','score']]
    comment_file = [['player','type','time','note']]
    for p in players:   
        for k, v in p.stats.items():                
            for kk, vv in v.items():
                if all([k, kk, vv]):
                    stat_file.append([p.name, k, kk, vv])
    for p in players:
        for i in p.feed:
            b = [x for x in i]
            b.insert(0, p)

            comment_file.append(b)
    list_tocsv(stat_file, 'player_stats.csv')
    list_tocsv(comment_file, 'player_feed.csv')



def load(pstats='player_stats.csv', pfeed='player_feed.csv'):
    import csv
    stats = [x for x in csv.reader(open(pstats,'rU'))][1:]
    feed = [x for x in csv.reader(open(pfeed, 'rU'))][1:]
    names = set([p[0] for p in stats])
    players = {}
    for name in names:
        pl = BasePlayer(BASE_STATS,name)
        players.update({name:pl})
    for x in stats:
        players[x[0]].stats[x[1]][x[2]]= int(x[3])

    for x in feed:
        players[x[0]].feed.append(x[1:])

    return players



BASE_STATS = {
    'offence':{
            'pass':0, 
            'dribble':0,
            'jumpshot':0,
            'layup':0,
            'freethrow':0,
            'assists':0,
        },
    'defence':{
            'blocking':0,
            'steal':0,
            'help':0,
            'pick':0,
        },
    'quality':{
            'hussle':0,
            'stamina':0,
            'leadership':0,
            'talent':0,
        }
}

import copy
class BasePlayer:
    def __init__(self, stats, name = "BasePlayer"):
        #start all players at 50
        for k, v in stats.items():
            for s in v:
                v[s] = 50
        self.stats = copy.deepcopy(stats)
        self.feed = []
        self.name = name
    def __str__(self):
        return self.name

    def add_stat(self, category, stat, value):
        self.stats[category][stat] += value
        self.feed.append(['stat',time.strftime("%c"),"{} {} {}".format(category,stat,value)])
    def show_stats(self, summary=False):
        if summary:
            for k, v in self.stats.items():
                print k
                for kk, vv in v.items():
                    if not int(vv) == 50:
                        print '   ', kk, vv
        else:

            for k, v in self.stats.items():
                print k
                for kk, vv in v.items():
                    print '   ', kk, vv

    def add_comment(self, comment):
        self.feed.append(['comment', time.strftime("%c"), comment])

    def print_feed(self, summary = False):
        print 
        if summary:
            for x in self.feed[:3]:
                print self.name,"-", x[1][4:10], "   ",x[2]

        else:
            for x in self.feed:
                print self.name,"", x[1][4:10], "   ",x[2]






class Gooey:
    def __init__(self, players = {}):
        self.players = players


    def validate_stat_command(self, commands):
        stats = [
            'freethrow',
            'layup',
            'assists',
            'pass',
            'jumpshot',
            'dribble',
            'pick',
            'steal',
            'blocking',
            'help',
            'hussle',
            'stamina',
            'leadership',
            'talent',
            ]
        if commands[0] in self.players.keys():
            if commands[1] in stats:
                try:
                    i = int(commands[2])
                    if i > -51 and i <50:

                        return True
                except:
                    pass
        print 'Invalid stat command'
        help()
        print 'Invalid stat command, please enter a valid command...'
        return False

    def process_commands(self, commands):
        if len(commands) == 1:
            c = commands[0]
            if c == 'players':
                print self.players.keys()

        # category, stat, value


        if len(commands) >=3 and  commands[1] == 'comment':
            if commands[0] in self.players.keys():
                print '----ADDING COMMENT---- {}'.format(" ".join(commands[2:]))
                self.players[commands[0]].add_comment(" ".join(commands[2:]))

        elif len(commands)  == 2 and commands[0] == 'add':
            print '----ADDING PLAYER---- {}'.format(commands[1])
            p = BasePlayer(BASE_STATS, commands[1])
            self.players.update({commands[1]:p})
        elif len(commands) ==2 and commands[0] == 'show' and commands[1] in self.players.keys():
            print '----PLAYER PROFILE----'
            self.players[commands[1]].show_stats()
            self.players[commands[1]].print_feed()
        elif len(commands) ==2 and commands[0] =='summary' and commands[1] in self.players.keys():
            print '----PLAYER SUMMARY----'
            self.players[commands[1]].show_stats(True)
            self.players[commands[1]].print_feed(True)
        elif len(commands) ==1 and commands[0] == 'feed':
            print 
            print '----FEED----'
            for x in self.players.values():
                x.print_feed(True)
        elif len(commands) == 1 and commands[0] == 'summary':
            print 
            print '----SUMARY----'
            for p in self.players.values():
                print '       ---',p.name,'---      '
                p.show_stats(True)
                p.print_feed(True)
                print
        elif len(commands) == 3:
            if self.validate_stat_command(commands):
                if commands[1] in BASE_STATS['offence']:
                    q = 'offence'
                if commands[1] in BASE_STATS['defence']:
                    q = 'defence'
                if commands[1] in BASE_STATS['quality']:
                    q = 'quality'
                self.players[commands[0]].add_stat(q, commands[1], int(commands[2]))
        elif len(commands) ==2 and commands[0] == 'feed' and commands[1] in self.players.keys():
            self.players[commands[1]].print_feed()

        else:
            help()
            print 'Please enter a valid command...'

        to_csv(self.players.values())





        return False
    def get_input(self):
        while True:
            inp = raw_input('command: ')
            commands = inp.split()
            self.process_commands(commands)
            print 
            print '---------------'
            print 





def start(keep = True):
    if os.path.isfile('player_stats.csv') and os.path.isfile('player_feed.csv') and keep:
        g = Gooey(load())
        print '---Players Loaded---'
        return g
    else:
        print '---Empty Database---'
        g = Gooey()
        return g



def create_test_players():
    GUI = start(False)

    '''GUI.players['tom'].show_stats()
    GUI.players['tom'].print_feed()'''
    commands = ['add tom', 'add brad', 'brad jumpshot 3', 'tom blocking 10', 'brad comment really good at dribbling', 'tom comment nice hussle']
    for x in commands:
        s = x.split(" ")
        GUI.process_commands(s)

    return GUI


#GUI = create_test_players()
commands = [
    ["add <player_name>                   ", "adds a player                          ",  'EXAMPLE: add tom'],
    ["<player_name> <skill> <points>      ", 'increases a players skill points       ', "EXAMPLE: tom jumpshot 10"],
    ["<player_name> comment <comment_text>", 'adds a comment to the players feed     ', 'EAMPLE: tom comment stamina is looking good'],
    ["summary                             ", "prints out a summary of your players stats and feed"],
    ['summary <player_name>               ', 'prints out summary of only that player'],
    ['show <player_name>                  ', 'prints out players full profile'],
    ['feed                                ', 'prints out the users feed which is the sorted events happening to the user'],
    ['feed <player_name>                  ', 'prints only the players feed']
]


def help():
    print 
    print '------------------------------COMMANDS------------------------------'
    print 
    for x in commands:
        print "  ".join(x)
    print
    print '------------------------------------------------------------'

GUI = start()
help()
print 
print 'Start by adding some players and info using the commands above!'
GUI.get_input()
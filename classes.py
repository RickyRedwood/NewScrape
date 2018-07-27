# classes.py
''' This file contains the classes for my scraper program '''

import re
from collections import OrderedDict

class Transaction:
    ''' This class is what will define the first part of the scraped record '''
    def __init__(self, instrument, xactdate, deedtype, county, notes=''):
        self.instrument = instrument
        self.xactdate = xactdate
        self.deedtype = deedtype
        self.county = county
        self.notes = notes

    def __setnotes(self, notes):
        if self.notes is None:
            self.notes = notes
        else:
            self.notes = self.notes + notes

    def get_instrument(self):
        return self.instrument

    def get_xactdate(self):
        # TODO need to decide if this is going to be type date or type string
        return self.xactdate

    def get_deedtype(self):
        billofsale = ('BOS',)
        cancelnod = ('CANCEL', 'CANDEF', 'CANNOD', 'CND', 'CNOD', 'CNTDF', 'PCND', 'RNOD',)
        clrelease = ('CLR', 'RCL', 'RELCL',)
        conditionaluse = ('CONUSE',)
        conservator = ('CONSD',)
        constlien = ('CL', 'C LIEN', 'CLIEN',)
        easements = ('EADN/C', 'EAS', 'EASA', 'EASAS', 'EASAGT', 'EASE', 'EASED', 'EASMT', 'ESMT',
                     'EASN/C', 'EASENC', 'EASWTR', 'ESMDEE', 'PEREAS',)
        exceptions = ('AAA', 'AACT',
                      'ACK', 'ACKM', 'ACOV', 'ACPOA', 'ACVPOA',
                      'ADDEND', 'ADMPLA', 'ADOM',
                      'AEAS',
                      'AFD', 'AF/DD', 'AFDEED', 'AFDMTG',
                      'AFF', 'AFFAFF', 'AFFDC', 'AFF&DC', 'AFFDM', 'AFFDTH', 'AFFIX', 'AFFI',
                      'AFFID', 'AFFMH', 'AFFMIS', 'AFFMS', 'AFFMTG', 'AFFNOP', 'AFFPOS', 'AFFSCR', 'AFFSUC',
                      'AFF/TR', 'AFFTRA', 'AFFTRF', 'AFFX', 'AFT',
                      'AGMT', 'AGMMTG', 'AGMTPL', 'AGR', 'AGR/MT', 'AGRMTG', 'AGRPLN', 'AGRPRL', 'AGTCRT',
                      'ALL', 'ALOR', 'ALSE',
                      'AMAGR', 'AMDOT', 'AMEASE', 'AMEMLE', 'AMEND', 'AMFS', 'AMMELE', 'AMRC', 'AMSA',
                      'AOC', 'AOR', 'AORD', 'AOST', 'AOV',
                      'APCU', 'APL', 'APP TR', 'APPMTG', 'APPST', 'APPT',
                      'ARENTS', 'ART',
                      'ASDOT', 'ASFF', 'ASGN', 'ASGTRT', 'ASL&R', 'ASLERT', 'ASMTG', 'ASMTLE', 'ASRENT', 'ASSEA',
                      'ASSGT',
                      'ASSI', 'ASSI/E', 'ASSIGN',
                      'ASSLSE', 'ASSN', 'ASSNLR', 'ASSR', 'ASSRNT', 'ASTR', 'ASSSUM',
                      'ATD', 'ATPPP', 'ATREDC', 'ATWOP',
                      'BCD', 'BCP', 'BOND',
                      'C DEED', 'C DOD',
                      'CA', 'CASSI',
                      'CCQCD',
                      'CD', 'CDC', 'CDEED', 'CDOR', 'CDOT',
                      'CEMD',
                      'CERDIS', 'CERMTG', 'CERT', 'CERTAM', 'CERTCT', 'CERTDC', 'CERTIF', 'CERTTR', 'CERTUS',
                      'CERWIL',
                      'CNOC', 'CNT',
                      'CODOR', 'COJTWD', 'CONTSA', 'CODEED',
                      'COEASE',
                      'COLN', 'COMDOT', 'CON', 'CONSLT', 'CONTFF', 'CONTRA', 'CONTRD',
                      'CORAFA', 'CORAFF', 'CORASG', 'CORD', 'CORDC', 'CORDOT', 'CORPRD', 'CORPRE', 'CORRAS', 'CORRD',
                      'CORRQD', 'CORPWD', 'CORRWD',
                      'CORSWD',
                      'CORTRD', 'CORTRU', 'CORWD', 'COT', 'COTTD', 'COV', 'COVE', 'COVEN', 'COWD',
                      'CP', 'CPA', 'CPLAT', 'CPOA', 'CPR D', 'CPRD', 'CPREPD',
                      'CQCD',
                      'CRWD',
                      'CSOT', 'CSUBA',
                      'CTA', 'CTDAOR',
                      'DBYTR',
                      'DC', 'DCERTD', 'DCTODD',
                      'DEATH', 'DECLA', 'DECLAR', 'DECRE', 'DECREE', 'DEDE', 'DEDI', 'DEDICA', 'DEM', 'DEMAND',
                      'DILF', 'DISHST',
                      'DOH',
                      'DPART',
                      'DRESCO',
                      'DSCH',
                      'ED', 'ESCNAG', 'ESTAFF', 'EXNOCM',
                      'FF', 'FFA', 'FFC', 'FFT',
                      'FINSTM', 'FIX', 'FIXQCD',
                      'FQCD',
                      'FROR',
                      'FS', 'FSAMDT', 'FSAMEN', 'FSC', 'FSCONT', 'FSPREL', 'FST', 'FSTERM',
                      'HOME',
                      'INDR',
                      'LEASE', 'LETTER',
                      'LIC', 'LICS',
                      'LMA', 'LMOD',
                      'LOTBCH', 'LOTSPL',
                      'LSA', 'LSE', 'LSO', 'LS&PL', 'LSPL', 'LSUB',
                      'LTCON', 'LTDSUB', 'LTSP',
                      'MACO', 'MCONR',
                      'MHAFF',
                      'MOA',
                      'NAO',
                      'NCN', 'NCOM',
                      'NOAL', 'NOAMDE',
                      'NOC', 'NCOM', 'NOE', 'NOS', 'NOT', 'NOTCOM', 'NOTEXT', 'NOTMTG', 'NOTICE', 'NOTN/C', 'NOTS',
                      'NOTTRS',
                      'NRFR',
                      'NTC', 'NTCCOM', 'NTCMTG', 'NTRSL',
                      'OPT', 'OPTION',
                      'ORD', 'ORDS',
                      'PA', 'PARWAL', 'PARTD', 'PARWD', 'PAT',
                      'PCON',
                      'PERPE',
                      'PLANDE', 'PLAT',
                      'PRAOR', 'PROCOV', 'PRPUB',
                      'PSA',
                      'PTRALR', 'PTREAL', 'PTTRUS',
                      'PURAGR', 'PUROP',
                      'RAOR', 'RATIFI', 'RCNL',
                      'RDOR',
                      'REAGRM', 'REAPP',
                      'RECIPT',
                      'REDEV', 'REDOT',
                      'REF',
                      'RELASN', 'RELASM', 'RELSRT', 'RELASR', 'REL-D', 'RELEAS', 'RELREC', 'RELSEV',
                      'RENO', 'RENUN',
                      'REPLAT',
                      'REQ', 'REQNOT', 'REQSUB', 'REQUE', 'REQUES', 'RES',
                      'REQCPY', 'REQREC',
                      'RERA', 'RESCIN', 'RESCOV', 'RESNF', 'RESOL', 'REST', 'RESTCV',
                      'RETAGM', 'RETAGR', 'REVTOD',
                      'RFN', 'RFNOD', 'RFR', 'RFTL',
                      'RIFIRE',
                      'RLCPA', 'RLSAOR', 'RLSASS', 'RLSMSC', 'RLSCON', 'RLSSA',
                      'RNDND', 'RNDNS', 'RNOT',
                      'ROR',
                      'RPLAT',
                      'RQRCVY',
                      'RRFR',
                      'RSA',
                      'RTODD',
                      'SA',
                      'SB MTG', 'SBA', 'SBAG', 'SBSR', 'SBT TR', 'SBTR', 'SBTRCE',
                      'SCORWD', 'SCRAFF', 'SDOT',
                      'SEC', 'SECAGR', 'SEV', 'SEVAGT', 'SEVCA',
                      'SID',
                      'SMTG',
                      'SOL', 'SOT',
                      'SP',
                      'STCONT', 'STMTAU', 'STXCON',
                      'SUB', 'SUBA', 'SUBAGM', 'SUBAGR', 'SUBAGT', 'SUBD', 'SUBDOR', 'SUBMTG', 'SUBO', 'SUBOMO',
                      'SUBORD',
                      'SUBTR', 'SUBTRU', 'SUR', 'SURN/C', 'SURREP', 'SURVEY',
                      'SWDC',
                      'TCIAC',
                      'TDM',
                      'TER', 'TERETC', 'TERM', 'TERMEA', 'TERMML', 'TERMTG', 'TERSA',
                      'TFIX', 'TLEASE', 'TLSE', 'TERLSE',
                      'TNOC',
                      'TODD',
                      'TPDR',
                      'TRAFF', 'TRDART',
                      'UAMD',
                      'UCCA', 'UCCC', 'UCCTER', 'UCC', 'UCCT', 'UCNT', 'UCT',
                      'UEVS',
                      'UFS', 'UTER',
                      'VOID',
                      'WAI', 'W/SLN', 'WAIVE', 'WAIVTD', 'WAVFR', 'WLRL', 'WOD', 'WVR',
                      'ZONE',)
        fedliens = ('FED', 'FEDTAX', 'FTXL')
        fedreleases = ('FEDREL', 'FEDRLS', 'FEDTER', 'FTERM', 'FTR', 'FTXREL',)
        lien = ('LIEN', 'UTLN',)
        lienrelease = ('LIENR', 'RELLN', 'RLSLN',)
        lispendens = ('LIS', 'LISPEN', 'NLP',)
        lispendensrelease = ('LISPRL', 'RLP',)
        mastercommisioner = ('MASTD', 'MCD',)
        mechlien = ('MECH', 'MLIEN',)
        memos = ('MEMAGM', 'MEMLEA', 'MEMLSE', 'MEM', 'MEMO', 'MEMOPT', 'MEMRED', 'MEMTRA', 'MHOEC', 'MOL',)
        modifications = ('ADDDOT', 'DOTMOD',
                         'MDOT', 'MOD', 'MOD DT', 'MODA', 'MODAGM', 'MODAGR', 'MODDOT', 'MODIFI', 'MODMTG', 'MODTRT',
                         'TDMOD', 'TRDMOD',)
        mortgages = ('CMDOT', 'CONDOT',
                     'D T', 'DISTD', 'DDOT', 'DISDOT', 'DISMTG', 'DOT', 'DOT2', 'DOTAR', 'DOT/AR', 'DOTASN',
                     'DOTASR', 'DOTASS', 'DOTAST', 'DOT/SA',
                     'MOR', 'MTG', 'MTGE', 'NOTE',
                     'SDDOT', 'SECDOT', 'SUBDOT',
                     'TD&AR', 'TRDAOR', 'TRDEED', 'TTAS',
                     'WAVDOT', 'WAIMTG',)
        miscnotes = ''
        nodlist = ('MECHLN', 'NOD', 'NTCDFT', 'NOTDEF',)
        partials = ('DOPR', 'PDOR', 'PR', 'PTDREC', 'PT REC', 'PT REL', 'PTMR', 'PTRECO', 'PTREL', 'STPREL',)
        persreps = ('D OF D', 'DDIS', 'DDIST', 'DDCPR', 'DISTB', 'DDPR', 'DOD', 'JTPRD',
                    'PRD', 'PRDEED', 'PRJTD', 'PRJTWD',)
        poas = ('AFPOA', 'DPOA', 'LTDPOA', 'POA', 'POAM',)
        propliens = ('PL',)
        quitclaims = ('JTQC', 'JTQCD', 'QCD',)
        releases = ('DOR',
                    'FREC', 'FRECON', 'FULLRC',
                    'MR',
                    'RECON', 'RECVY', 'REL', 'RELMTG', 'RLS', 'RLEASE', 'RLS-MG',
                    'SAT', 'SATIS', 'SBTRDR', 'SDOR', 'SOTDOR', 'SOTREC', 'ST&DR', 'SUB/RE', 'SUTRDR', 'SUBTRDR',
                    'TDOR', 'TR D R', 'TRDORT', 'TRREG', 'TRSREC', 'TRUSRE',)
        sheriffdeed = ('SD', 'SHERD',)
        stateliens = ('STL', 'STTAX', 'STXL',)
        statereleases = ('STT', 'STTERM', 'STXT', 'STXTER',)
        taxdeeds = ('TREATD',)
        tempeasement = ('TEMEAS',)
        treasurerdeeds = ('TXDEED',)
        trusteedeeds = ('DINTR', 'DIT',
                        'SCTD',  # Successor Co-Trustees Deed in Hamilton County
                        'TD', 'TDOD', 'TJTD', 'TRASST', 'TRD', 'TREED',
                        'TRS D', 'TRSD', 'TRSJTD', 'TRSWD', 'TRTD', 'TRUSTD', 'TSD', 'TWD', 'TRWTY',)
        warrantydeeds = ('CJTWD', 'CORPD', 'CORPWD', 'CWD',
                         'DEED',
                         'JTD', 'JTDPOA', 'JTWD',
                         'LLCJTD', 'LLCWD',
                         'PARTWD', 'PRTWD', 'PTNRWD', 'PWD',
                         'SPWD', 'SPWTY', 'SRVWTY', 'SWD',
                         'TXDEED',
                         'WD', 'WTY',)

        if self.deedtype in warrantydeeds:
            deedtype = 'Warranty'
        elif self.deedtype in conservator:
            deedtype = 'Warranty'
            miscnotes = "(Conservator's Deed)"
        elif self.deedtype in taxdeeds:
            deedtype = 'Warranty'
            miscnotes = "(Treasurer's Tax Deed)"
        elif self.deedtype in sheriffdeed:
            deedtype = 'Warranty'
            miscnotes = miscnotes + "(Sheriff's Deed)"
        elif self.deedtype in mastercommisioner:
            deedtype = 'Warranty'
            miscnotes = miscnotes + "(Master Commissioner's Deed)"
        elif self.deedtype in treasurerdeeds:
            deedtype = 'Warranty'
            miscnotes = miscnotes + "(Treasurer's Tax Deed)"
        elif self.deedtype in quitclaims:
            deedtype = 'Quitclaim'
        elif self.deedtype in persreps:
            deedtype = 'Pers Rep'
        elif self.deedtype in trusteedeeds:
            deedtype = 'Trustee'
        elif self.deedtype in mortgages:
            deedtype = 'DOT'
            isdeed = True
        elif self.deedtype in modifications:
            deedtype = 'DOT'
            miscnotes = miscnotes + '(Modification)'
        elif self.deedtype in releases:
            deedtype = 'DOR'
        elif self.deedtype in partials:
            deedtype = 'DOR'
            miscnotes = miscnotes + '(Partial)'
        elif self.deedtype in nodlist:
            deedtype = 'NOD'
        elif self.deedtype in constlien:
            deedtype = 'NOD'
            miscnotes = miscnotes + '(Construction Lien)'
        elif self.deedtype in mechlien:
            deedtype = 'NOD'
            miscnotes = miscnotes + "(Mechanic's Lien )"
        elif self.deedtype in lispendens:
            deedtype = 'NOD'
            miscnotes = miscnotes + '(Notice of Lis Pendens)'
        elif self.deedtype in lispendensrelease:
            deedtype = 'Cancel NOD'
            miscnotes = miscnotes + '(Release of Lis Pendens)'
        elif self.deedtype in cancelnod:
            deedtype = 'Cancel NOD'
            if self.deedtype == 'PCND':
                miscnotes = miscnotes + '(Partial Cancellation of Notice of Default)'
        elif self.deedtype in clrelease:
            deedtype = 'Cancel NOD'
            miscnotes = miscnotes + '(Construction Lien Release)'
        elif self.deedtype in lienrelease:
            deedtype = 'Cancel NOD'
            miscnotes = miscnotes + '(Lien Release)'
        elif self.deedtype in billofsale:
            deedtype = 'Misc'
            miscnotes = miscnotes + '(Bill of Sale)'
        elif self.deedtype in easements:
            deedtype = 'Misc'
            miscnotes = miscnotes + '(Easement)'
        elif self.deedtype in conditionaluse:
            deedtype = 'Misc'
            miscnotes = miscnotes + '(Conditional Use Permit)'
        elif self.deedtype in lien:
            deedtype = 'NOD'
            miscnotes = miscnotes + '(Lien)'
        elif self.deedtype in fedliens:
            deedtype = 'Fed Lien'
        elif self.deedtype in fedreleases:
            deedtype = 'Fed Rel'
        elif self.deedtype in memos:
            deedtype = 'Misc'
            miscnotes = miscnotes + '(Memo)'
        elif self.deedtype in poas:
            deedtype = 'Misc'
            miscnotes = miscnotes + '(Power of Attorney)'
        elif self.deedtype in propliens:
            deedtype = 'Misc'
            miscnotes = miscnotes + '(Property Lien)'
        elif self.deedtype in stateliens:
            deedtype = 'State Lien'
        elif self.deedtype in statereleases:
            deedtype = 'State Rel'
        elif self.deedtype in tempeasement:
            deedtype = 'Misc'
            miscnotes = miscnotes + '(Temporary Easement)'
        elif self.deedtype in exceptions:
            deedtype = 'Exception'
        else:
            deedtype = self.deedtype

        # catch the counties that use a different abbreviation than above
        if self.county == 46 and self.deedtype == 'TD':  # Merrick
            deedtype = 'DOT'
        if self.county == 31 and self.deedtype == 'TD':  # Burt
            deedtype = 'DOT'
        if self.county == 10 and self.deedtype == 'TD':  # Platte
            deedtype = 'DOT'
        if self.county == 28 and self.deedtype == 'TD':  # Hamilton
            deedtype = 'DOT'
        if self.county == 27 and self.deedtype == 'TRTD':  # Wayne
            deedtype = 'Trustee'
        if self.county == 25 and self.deedtype == 'CONDOT':  # Butler
            deedtype = 'NOD'
            miscnotes = miscnotes + '(Construction Lien)'

        # need to update the notes, but don't need to touch the self.deedtype because I can return the string
        self.__setnotes(miscnotes)
        return deedtype

    def get_county(self):
        # I'm only doing this so I don't have to worry about doing it if I grow
        countydict = {
            1: 'Douglas',
            2: 'Lancaster',
            3: 'Gage',
            4: 'Custer',
            5: 'Dodge',
            6: 'Saunders',
            7: 'Madison',
            8: 'Hall',
            9: 'Buffalo',
            10: 'Platte',
            11: 'Otoe',
            12: 'Knox',
            13: 'Cedar',
            14: 'Adams',
            15: 'Lincoln',
            16: 'Seward',
            17: 'York',
            18: 'Dawson',
            19: 'Richardson',
            20: 'Cass',
            21: 'Scotts Bluff',
            22: 'Saline',
            23: 'Boone',
            24: 'Cuming',
            25: 'Butler',
            26: 'Antelope',
            27: 'Wayne',
            28: 'Hamilton',
            29: 'Washington',
            30: 'Clay',
            31: 'Burt',
            32: 'Thayer',
            33: 'Jefferson',
            34: 'Fillmore',
            35: 'Dixon',
            36: 'Holt',
            37: 'Phelps',
            38: 'Furnas',
            39: 'Cheyenne',
            40: 'Pierce',
            41: 'Polk',
            42: 'Nuckolls',
            43: 'Colfax',
            44: 'Nemaha',
            45: 'Webster',
            46: 'Merrick',
            47: 'Valley',
            48: 'Red Willow',
            49: 'Howard',
            50: 'Franklin',
            51: 'Harlan',
            52: 'Kearney',
            53: 'Stanton',
            54: 'Pawnee',
            55: 'Thurston',
            56: 'Sherman',
            57: 'Johnson',
            58: 'Nance',
            59: 'Sarpy',
            60: 'Frontier',
            61: 'Sheridan',
            62: 'Greeley',
            63: 'Boyd',
            64: 'Morrill',
            65: 'Box Butte',
            66: 'Cherry',
            67: 'Hitchcock',
            68: 'Keith',
            69: 'Dawes',
            70: 'Dakota',
            71: 'Kimball',
            72: 'Chase',
            73: 'Gosper',
            74: 'Perkins',
            75: 'Brown',
            76: 'Dundy',
            77: 'Garden',
            78: 'Deuel',
            79: 'Hayes',
            80: 'Sioux',
            81: 'Rock',
            82: 'Keya Paha',
            83: 'Garfield',
            84: 'Wheeler',
            85: 'Banner',
            86: 'Blaine',
            87: 'Logan',
            88: 'Loup',
            89: 'Thomas',
            90: 'McPherson',
            91: 'Arthur',
            92: 'Grant',
            93: 'Hooker'
        }
        return countydict[self.county]

    def get_notes(self):
        return self.notes

    def add_notes(self, notes):
        return self.notes + notes

class BuyerSeller(Transaction):
    def __init__(self, name):
        #Transaction.__init__(self, instrument, xactdate, deedtype, county, notes='')
        self.name = name

    def __iter__(self):
        self.n = 0
        return self

    def __len__(self):
        return len(self.name)

    def __next__(self):
        if self.n <= len(self.name) - 1:
            thisname = self.name[self.n]
            self.n += 1
            return thisname
        else:
            raise StopIteration

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def fix_name(self, namelist):
        ''' This method must be called from the program and its parameter should be the object's get_name()
        method where that method has an index. Example:
        name = grantor.fix_name(grantor.get_name()[x])'''

        # RegExes of bank names goes here
        # TODO Banks that have partnered with MERS i.e., MERS/Guaranteed Rate Mortgage LLC, need to have the MERS part added to their regex search
        # TODO Need to add credit unions
        # TODO Need to add mortgage companies and non-bank lenders to this list
        reAcademyMort = re.compile(r'ACADEMY MORTGAGE.*')
        reAccessBank = re.compile(r'ACCESS ?BANK.*')  # Access Bank
        reAccessMort = re.compile(r'(?:MERS/)?ACCESS NATIONAL MORTGAGE.*')
        reAdmiralsBank = re.compile(r'ADMIRALS BANK.*')  # Admirals Bank
        reAgriBank = re.compile(r'^AGRIBANK.*')  # AgriBank
        reAIB = re.compile(r'AMERICAN INTERSTATE BANK.*')  # American Interstate Bank
        reAmerican = re.compile(r'AMERICAN MORTGAGE.*')
        reAmerisave = re.compile(r'AMERISAVE MORTGAGE.*')
        reANB = re.compile(r'AMERICAN NAT(IONA)?L BANK.*')  # American National Bank
        reAmerSW = re.compile(r'(?:MERS/)?AMERICAN SOUTHWEST MORTGAGE.*')
        reArborBank = re.compile(r'ARBOR BANK.*')  # Arbor Bank
        reArcher = re.compile(r'ARCHER CO-?OP(?:ERATIVE)? C(?:REDIT) ?U(?:NION)?.*')
        reArkLaTex = re.compile(r'ARK-LA-TEX.*')
        reAuburnState = re.compile(r'AUBURN STATE BANK.*')  # Auburn State Bank
        reBankFirst = re.compile(r'BANK ?FIRST.*')  # BankFirst
        reBankAmer = re.compile(r'BANK OF AMERICA.*')
        reBankDoniphan = re.compile(r'BANK OF DONIPHAN.*')
        reBankHartington = re.compile(r'BANK OF HARTINGTON.*')
        reBankLindsay = re.compile(r'BANK OF LINDSAY.*')
        reBankMarquette = re.compile(r'BANK OF MARQUETTE.*')
        reBankMead = re.compile(r'BANK OF MEAD.*')
        reBankNYMellon = re.compile(r'BANK OF NEW YORK MELLON.*')
        reBankNewmanGrove = re.compile(r'BANK OF NEWMAN GROVE.*')
        reBankPrague = re.compile(r'BANK OF PRAGUE.*')
        reBankValley = re.compile(r'BANK OF THE VALLEY.*')
        reBankWest = re.compile(r'BANK OF THE WEST.*')
        reBattleCreek = re.compile(r'BATTLE CREEK STATE BANK.*')  # Battle Creek State Bank
        reBaxter = re.compile(r'BAXTER C(?:REDIT)? ?U(?:NION).*')
        reBayview = re.compile(r'BAYVIEW LOAN SERVICING.*')
        reBBMC = re.compile(r'BBMC MORTGAGE.*')
        reBMOHarris = re.compile(r'BMO HARRIS BANK.*')  # BMO Harris Bank
        reBrunswick = re.compile(r'BRUNSWICK STATE BANK.*')  # Brunswick State Bank
        reCaliber = re.compile(r'CALIBER HOME LOANS.*')
        reCapitol = re.compile(r'CAPITOL FEDERAL SAVINGS BANK.*')
        reCapCity = re.compile(r'(?:MERS/)?CAPITAL CITY MORTGAGE.*')
        reCarrington = re.compile(r'CARRINGTON MORTGAGE SERVICES.*')
        reCassCo = re.compile(r'CASS COUNTY BANK.*')
        reCastleCooke = re.compile(r'(?:MERS/)?CASTLE & COOKE.*')
        reCattleNatl = re.compile(r'CATTLE (NAT(IONA)?L )?B(ANK)? & T.*')
        reCedarSec = re.compile(r'CEDAR SECURITY BANK.*')
        reCentralBk = re.compile(r'CENTRAL BANK.*')  # Central Bank Div of Citizens Bank & Trust
        reCentralNatlBk = re.compile(r'(?:MERS/)?CENTRAL NAT(IONA)?L BANK.*')  # Central National Bank
        reCentNebrFCU = re.compile(r'CENTRAL NEBR(?:ASKA) F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reCentris = re.compile(r'CENTRIS F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reCerescoBank = re.compile(r'CERESCO ?BANK.*')  # CerescoBank
        reCharlesSchwab = re.compile(r'CHARLES SCHWAB BANK.*')
        reCharterWest = re.compile(r'(?:MERS/)?CHARTER ?WEST BANK.*')
        reChurchill = re.compile(r'CHURCHILL MORTGAGE.*')
        reCitiBank = re.compile(r'(?:MERS/)?CITIBANK.*')
        reCitiCorp = re.compile(r'CITICORP TRUST BANK.*')
        reCitiMort = re.compile(r'(?:MERS/)?CITIMORTGAGE.*')
        reCitizensBT = re.compile(r'CITIZENS B(?:ANK)? (AND|&) T(?:RUST)?.*')  # Citizens Bank & Trust
        reCitizensState = re.compile(r'CITIZENS STATE BANK.*')
        reCityBank = re.compile(r'CITY B(?:ANK)? (AND|&) T(?:RUST)?.*')
        reClarksonBk = re.compile(r'CLARKSON BANK.*')
        reCMG = re.compile(r'CMG MORTGAGE Inc.*')
        reCoBank = re.compile(r'COBANK.*')
        reCBT = re.compile(r'COL(?:UMBU)?S B(?:ANK)? (&|AND) T((?:RUST)? CO(?:MPANY)?)?,*')
        reColsFCU = re.compile(r'COL(?:UMBU)?S UNITED F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reCommBank = re.compile(r'COMM(?:ERCIAL)? STATE BANK.*')
        reCCC = re.compile(r'COMMODITY CREDIT CORP.*')
        reCmtyBank = re.compile(r'COMM(?:UNITY)? BANK.*')
        reCoreBank = re.compile(r'(?:MERS/)?CORE BANK.*')
        reCornerstone = re.compile(r'CORNERSTONE BANK.*')
        reCornhusker = re.compile(r'CORNHUSKER BANK.*')
        reCrestar = re.compile(r'CRESTAR MORTGAGE.*')
        reCrossCountry = re.compile(r'CROSSCOUNTRY MORTGAGE.*')
        reCrossFirst = re.compile(r'CROSSFIRST BANK.*')
        reDaleFCU = re.compile(r'DALE EMPLOYEES F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reDeutsche = re.compile(r'DDEUTSCHE BANK (?:NATIONAL )?TRUST CO.*')
        reDiscover = re.compile(r'DISCOVER BANK.*')
        reDLJ = re.compile(r'DLJ MORTGAGE CAPITAL.*')
        reDundee = re.compile(r'DUNDEE BANK.*')
        reEVBT = re.compile(r'ELKHORN VALLEY B(?:ANK)?( ?(&|AND) TRUST( CO(RP|PR))?)?.*')
        reEmbrace = re.compile(r'EMBRACE HOME LOANS.*')
        reEnterprise = re.compile(r'ENTERPRISE BANK.*')
        reEquitable = re.compile(r'EQUITABLE BANK.*')
        reExchBT = re.compile(r'EXCHANGE BANK & TRUST.*')
        reExchGib = re.compile(r'EXCHANGE BANK OF GIBBON.*')
        reExchange = re.compile(r'EXCHANGE BANK.*')
        reFM = re.compile(r'F(ARMERS)? ?(&|AND) ?M(ERCHANTS)? BANK.*')
        reFCLSC = re.compile(r'FARM CREDIT LEASING SERVICES CORP.*')
        reFCSA = re.compile(r'FARM CREDIT S(?:ER)?V(?:ICE)?S? ?(?:OF)? ?(?:AMERICA)?.*')
        reFCSM = re.compile(r'FARM CREDIT SERVICES OF THE MIDLANDS.*')
        reFSA = re.compile(r'FARM SERVICE AGENCY.*')
        reFarmers = re.compile(r'FARMERS STATE BANK.*')
        reFedTopeka = re.compile(r'FED(ERAL)? HOME LOAN BANK (:?OF )?TOPEKA')
        reFedMort = re.compile(r'FEDERAL HOME LOAN MORTGAGE CORP.*')
        reFannieMae = re.compile(r'FED(?:ERAL)? NAT(?:IONA)?L M(?:OR)?TG(?:AGE)? ASS(?:OCIATIO)?N.*')
        reFidelity = re.compile(r'FIDELTIY NATIONAL.*')
        reFieldstone = re.compile(r'(?:MERS/)?FIELDSTONE MORTGAGE COMPANY.*')
        re5th3rd = re.compile(r'FIFTH THIRD BANK.*')
        reFirstAmerSvgs = re.compile(r'FIRST AMERICAN SAVINGS BANK.*')
        reFATIC = re.compile(r'FIRST AMER(ICAN)? TITLE(?: INS(URANCE)? CO)?.*')
        reFirstBancroft = re.compile(r'FIRST BANK OF BANCROFT.*')
        reFirstUtica = re.compile(r'FIRST BANK OF UTICA.*')
        reFirstCmty = re.compile(r'FIRST COMMUNITY BANK.*')
        reFirstDak = re.compile(r'FIRST DAKOTA NAT(IONA)?L BANK.*')
        reFirstMagnus = re.compile(r'(?:MERS/)?FIRST MAGNUS FINANCIAL CORP.*')
        reFirstKey = re.compile(r'FIRSTKEY MORTGAGE.*')
        reFirstMidwest = re.compile(r'FIRST MIDWEST BANK.*')
        reFirstMort = re.compile(r'(?:MERS/)?FIRST MORTGAGE CO.*')
        reFirstNebr = re.compile(r'FIRST N(A|E)BR(?:ASKA)? BANK')
        re1nbt = re.compile(r'FIRST NATIONAL BANK & TRUST CO.*')
        re1nbne = re.compile(r'FIRST NAT(?:IONA)?L BANK N(?:ORTH)?E(?:AST)?.*')
        refnbo = re.compile(r'FIRST NAT(?:IONA)?L BANK ?,?(?:OF )?OMAHA.*')
        re1nbFairbury = re.compile(r'FIRST NATIONAL BANK, ?FAIRBURY')
        re1nCU = re.compile(r'FIRST NEBRASKA CREDIT UNION.*')
        re1neCU = re.compile(r' FIRST NEBRASKA EDUCATORS CREDIT UNION.*')
        re1nenebr = re.compile(r'FIRST N(?:ORTH)?E(?:AST)? BANK OF NEBR(?:ASKA)?.*')
        re1Premier = re.compile(r'FIRST PREMIER BANK.*')
        re1sbt = re.compile(r'FIRST STATE BANK (&|AND) TRUST CO.*')
        re1sbNebr = re.compile(r'FIRST STATE BANK NEBR(?:ASKA)?.*')
        re1sb = re.compile(r'FIRST STATE BANK.*')
        reFirstTri = re.compile(r'FIRST TRI-? ?COUNTY BANK.*')
        reFirstWestroads = re.compile(r'FIRST WESTROADS BANK.*')
        reFirstBank = re.compile(r'FIRSTBANK OF NEBRASKA.*')
        reFivePts = re.compile(r'FIVE POINTS BANK.*')
        reFlagstar = re.compile(r'FLAGSTAR BANK.*')
        reFortress = re.compile(r'FORTRESS CREDIT CO.*')
        reFoundationOne = re.compile(r'FOUNDATION ONE BANK.*')
        re4pts = re.compile(r'FOUR POINTS F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reFranklin = re.compile(r'FRANKLIN AMERICAN MORTGAGE.*')
        reFreedom = re.compile(r'FREEDOM MORTGAGE.*')
        reFrontier = re.compile(r'FRONTIER BANK.*')
        reGateway = re.compile(r'GATEWAY MORTGAGE GROUP.*')
        reGenerations = re.compile(r'GENERATIONS BANK.*')
        reGreatPlains = re.compile(r'GREAT PLAINS STATE BANK.*')
        reGSB = re.compile(r'GREAT SOUTHERN BANK.*')
        reGWB = re.compile(r'(?:MERS/)?GREAT WESTERN BANK.*')
        reHeartland = re.compile(r'HEARTLAND BANK.*')
        reHenderson = re.compile(r'HENDERSON STATE BANK.*')
        reHeritage = re.compile(r'HERITAGE BANK.*')
        reHFSL = re.compile(r'HOME FED(?:ERAL)? S(?:AVINGS)? (&|AND) L(?:OAN)? ASS(?:OCIATIO)?N')
        reHomeLoan = re.compile(r'HOME LOAN INVESTMENT BANK.*')
        reHomestead = re.compile(r'HOMESTEAD BANK.*')
        reHorizon = re.compile(r'HORIZON BANK.*')
        reHSBC = re.compile(r'HSBC BANK.*')
        reIowaBankMort = re.compile(r'IOWA BANKERS MORTGAGE CORP.*')
        reJeffCo = re.compile(r'JEFFERSON COUNTY BANK.*')
        reJones = re.compile(r'JONES NAT(?:IONA)?L BANK.*')
        reJPMorgan = re.compile(r'J\.?P\.? ?MORGAN CHASE BANK.*')
        reJPMorganMort = re.compile(r'J\.?P\.? ?MORGAN MORTGAGE.*')
        reLakeview = re.compile(r'(?:MERS/)?LAKEVIEW LOAN SERVICING.*')
        reLiberty = re.compile(r'(?:MERS/)?LIBERTY FIRST C(?:REDIT)? ?U(?:NION)?.*')
        reLincolnFSB = re.compile(r'(?:MERS/)?LINCOLN F(?:EDERAL)? ?S(?:AVINGS)? ?B(?:ANK)? (?:OF )?NE(BR)?(ASKA)?.*')
        reLoanDepot = re.compile(r'LOANDEPOT\.COM.*')
        reLocher = re.compile(r'LOCHER')  # trustee for US Bank
        reMalvern = re.compile(r'MALVERN BANK.*')
        reMCB = re.compile(r'MADI(OS|SO)N COUNTY BANK.*')
        reMember = re.compile(r'MEMBERS? MORTGAGE SERVICES.*')
        reMembersOwn = re.compile(r'MEMBERSOWN CREDIT UNION.*')
        reMERS = re.compile(r'(MERS.*|M(?:OR)?TG(?:AGE)? ELEC(\. ?|TRONIC )REGIS(?:TRATION)? SYSTEMS.*)')
        reMetro = re.compile(r'METRO CREDIT UNION MORTGAGE.*')
        reMetroLife = re.compile(r'METROP(OL|LO)ITAN LIFE INS(?:URANCE)? CO(?:MPANY)?.*')
        reMidAmer = re.compile(r'MID ?AMERICA MORTGAGE.*')
        reMidwest = re.compile(r'MIDWEST BANK.*')
        reMoria = re.compile(r'(?:MERS/)?MORIA DEVELOPMENT.*')
        reMtgRes = re.compile(r'(?:MERS/)?MORTGAGE RESEARCH CENTER.*')
        reMtgSpec = re.compile(r'MORTGAGE SPECIALISTS.*')
        reMut1FCU = re.compile(r'MUTUAL FIRST F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reMutOmaha = re.compile(r'MUTUAL OF OMAHA( BANK)?.*')
        reNAFCO = re.compile(r'NAFCO NE FEDERAL CREDIT UNION.*')
        reNavy = re.compile(r'NAVY F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reNationstar = re.compile(r'NATIONSTAR MORTGAGE.*')
        reNebrComm = re.compile(r'NE(?:BR)?(?:ASKA) BANK OF COMMERCE.*')
        reNebrEnergyFCU = re.compile(r'NEBR(?:ASKA)? ?ENERGY F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reNIFA = re.compile(r'NEBR(?:ASKA)? INVESTMENT FIN(?:ANCE)? AUTH(?:ORITY)?.*')
        reNebrEDC = re.compile(r'NE(?:BR)?(?:ASKA)? ECON(?:OMIC)? DEV(?:ELOPMENT)? CORP.*')
        reNebrStBk = re.compile(r'NEBRASKA STATE BANK OF OMAHA')
        reNewPenn = re.compile(r'NEW PENN FINANCIAL.*')
        reNewRes = re.compile(r'NEW RESIDENTIAL MORTGAGE.*')
        reNASB = re.compile(r'(?:MERS/)?NORTH AMERIAN SAVINGS BANK.*')
        reNENebrFCU = re.compile(r'N(?:ORTH)?E(?:AST)? NE(?:BRASKA)? F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reNWBk = re.compile(r'NORTHWEST BANK.*')
        reOakCrk = re.compile(r'OAK CREEK VALLEY BANK.*')
        reOcwen = re.compile(r'OCWEN LOAN SERVICING.*')
        reOldRep = re.compile(r'OLD REPUBLIC NATIONAL TITLE INSURANCE CO.*')
        reOmahaFCU = re.compile(r'OMAHA F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reParamount = re.compile(r'PARAMOUNT RESIDENTIAL MORTGAGE GROUP.*')
        rePathway = re.compile(r'PATHWAY BANK.*')
        rePennyMac = re.compile(r'PENNYMAC LOAN SERVICES.*')
        rePinnBank = re.compile(r'PINNACLE BANK.*')
        rePVB = re.compile(r'PLATTE VALLEY BANK.*')
        rePNC = re.compile(r'PNC BANK.*')
        rePNCMort = re.compile(r'PNC MORTGAGE.*')
        rePrivateMtg = re.compile(r'(?:THE)? ?PRIVATE MORTGAGE GROUP.*')
        rePremier = re.compile(r'PREMIER BANK.*')
        rePremierHome = re.compile(r'PREMIER HOME MORTGAGE.*')
        rePremierLending = re.compile(r'(?:MERS/)?PREMIER LENDING ALLIANCE.*')
        rePrincipalResMtg = re.compile(r'(?:MERS/)?PRINCIPAL RESIDENTIAL MORTGAGE.*')
        reQuicken = re.compile(r'(?:MERS/)?QUICKEN LOANS?.*')
        reRegent = re.compile(r'(?:MERS/)?REGENT FINANCIAL GROUP.*')
        reReverse = re.compile(r'REVERSE MORTGAGE SOLUTIONS.*')
        reSAC = re.compile(r'SAC F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reSantander = re.compile(r'SANTANDER BANK.*')
        reSecBk = re.compile(r'SECURITY BANK.*')
        reSec1Bk = re.compile(r'SECURITY FIRST BANK.*')
        reSecHome = re.compile(r'SECURITY HOME BANK.*')
        reSecNatl = re.compile(r'SECURITY NAT(?:IONA)?L BANK.*')
        reSecState = re.compile(r'SECURITY STATE BANK.*')
        reSilk = re.compile(r'SILK ABSTRACT COMPANY.*')
        reSirva = re.compile(r'(?:MERS/)?SIRVA MORTGAGE.*')
        reSBA = re.compile(r'SMALL BUSINESS ADMINISTRATION.*')
        reSpecLoan = re.compile(r'SPECIALIZED LOAN SERVICING.*')
        reSpiritAmer = re.compile(r'SPIRIT OF AMERICAN F(?:ED)?(?:ERAL)? ?C(?:REDIT)? ?U(?:NION)?.*')
        reStanton = re.compile(r'STANTON STATE BANK.*')
        reStewart = re.compile(r'STEWART TITLE GUARANTY COMPANY.*')
        reColon = re.compile(r'STATE BANK OF COLON.*')
        reStateFarm = re.compile(r'STATE FARM BANK.*')
        reStateNebr = re.compile(r'STATE NEBRASKA BANK.*')
        reSuntrust = re.compile(r'SUNTRUST MORTGAGE.*')
        reTIAA = re.compile(r'TIAA.*')
        reTierOne = re.compile(r'TIERONE BANK.*')
        reTilden = re.compile(r'TILDEN BANK.*')
        re2rb = re.compile(r'TWO RIVERS (?:STATE )?BANK')
        reUSAA = re.compile(r'(?:MERS/)?USAA FEDERAL SAVINGS BANK.*')
        reUSBank = re.compile(r'\bU(\.| )?S(\.| )? BANK.*')  # looks for forms of US Bank
        reUBT = re.compile(r'(?:MERS/)?UNION BANK (&|AND) ?(TRUST ?CO)?.*')
        reUnitedFidelity = re.compile(r'(?:MERS/)?UNITED FIDELITY FUNDING CORP.*')
        reUnitedRep = re.compile(r'UNITED REPUBLIC BANK.*')
        reUSHome = re.compile(r'(?:MERS/)?US HOME MORTGAGE.*')
        reValley = re.compile(r'VALLEY BANK & TRUST.*')
        reVeridian = re.compile(r'VERIDIAN C(?:REDIT)? ?U(?:NION)?.*')
        reWSB = re.compile(r'WAHOO STATE BANK.*')
        reWCB = re.compile(r'WASHINGTON COUNTY BANK.*')
        reWaypoint = re.compile(r'WAYPOINT BANK.*')
        reWFB = re.compile(r'WELLS FARGO BANK.*')
        reWFF = re.compile(r'WELLS FARGO FIN(\.|ANCIAL)? *(?:NAT(?:IONA)?L)? BANK.*')
        reWestgate = re.compile(r'WEST (AGTE|GATE) BANK.*')
        reWestern = re.compile(r'WESTERN NATIONAL BANK.*')
        reWilmington = re.compile(r'WILMINGTON SA?V(?:IN)?GS FUND SOCIETY.*')
        reWyndham = re.compile(r'WYNDHAM CAPITAL MORTGAGE.*')
        reYork = re.compile(r'YORK STATE BANK.*')

        # regex of business suffixes goes here
        reChurch = re.compile(r'\sCHURCH\s')
        reCompany = re.compile(r'CO(MPANY)? ?(?! PERS(ONAL)? REP(RESENTATIVE)?)\s')
        reCorp = re.compile(r'\sCORP(ORATION)?\s')
        reFarms = re.compile(r'\sFARMS?\s')
        reInc = re.compile(r'\sINC(ORPORATED)?\s')
        reLLC = re.compile(r'\sL?\.?L\.?(C|P)\.?\s')
        reLTD = re.compile(r'\sLTD\s')
        rePC = re.compile(r'\sPC\s')

        # This is where we setup the dictionary that will look up the keys and place the proper
        # values for the bank names

        mybank = {
            reAcademyMort: 'Academy Mortgage Corporation',
            reAccessBank: 'Access Bank',
            reAccessMort: 'Access National Mortgage',
            reAdmiralsBank: 'Admirals Bank',
            reAgriBank: 'AgriBank',
            reAIB: 'American Interstate Bank',
            reAmerican: 'American Mortgage Company',
            reAmerisave: 'Amerisave Mortgage Corporation',
            reANB: 'American National Bank',
            reAmerSW: 'American Southwest Mortgage Corp',
            reArborBank: 'Arbor Bank',
            reArcher: 'Archer Cooperative Credit Union',
            reArkLaTex: 'Ark-La-Tex Financial Services LLC',
            reAuburnState: 'Auburn State Bank',
            reBankAmer: 'Bank of America',
            reBankDoniphan: 'Bank of Doniphan',
            reBankFirst: 'BankFirst',
            reBankHartington: 'Bank of Hartington',
            reBankLindsay: 'Bank of Lindsay',
            reBankMarquette: 'Bank of Marquette',
            reBankMead: 'Bank of Mead',
            reBankNYMellon: 'Bank of New York Mellon',
            reBankNewmanGrove: 'Bank of Newman Grove',
            reBankPrague: 'Bank of Prague',
            reBankValley: 'Bank of the Valley',
            reBankWest: 'Bank of the West',
            reBattleCreek: 'Battle Creek State Bank',
            reBaxter: 'Baxter Credit Union',
            reBayview: 'Bayview Loan Servicing LLC',
            reBBMC: 'BBMC Mortgage',
            reBMOHarris: 'BMO Harris Bank',
            reBrunswick: 'Brunswick State Bank',
            reCaliber: 'Caliber Home Loans Inc',
            reCapitol: 'Capitol FSB',
            reCapCity: 'Capital City Mortgage',
            reCarrington: 'Carrington Mortgage Services LLC',
            reCassCo: 'Cass County Bank',
            reCastleCooke: 'Castle & Cooke Mortgage LLC',
            reCattleNatl: 'Cattle National Bank & Trust',
            reCedarSec: 'Cedar Security Bank',
            reCentralBk: 'Central Bank',
            reCentralNatlBk: 'Central National Bank',
            reCentNebrFCU: 'Central Nebraska Federal Credit Union',
            reCentris: 'Centris Federal Credit Union',
            reCerescoBank: 'CerescoBank',
            reCharlesSchwab: 'Charles Schwab Bank',
            reCharterWest: 'CharterWest Bank',
            reChurchill: 'Churchill Mortgage Corporation',
            reCitiBank: 'CitiBank',
            reCitiCorp: 'CitiCorp',
            reCitiMort: 'CitiMortgage',
            reCitizensBT: 'Citizens Bank & Trust',
            reCitizensState: 'Citizens State Bank',
            reCityBank: 'City Bank & Trust',
            reClarksonBk: 'Clarkson Bank',
            reCMG: 'CMG Mortgage Inc',
            reCoBank: 'CoBank',
            reCBT: 'Columbus Bank & Trust Company',
            reColsFCU: 'Columbus United Federal Credit Union',
            reCommBank: 'Commercial State Bank',
            reCCC: 'Commodity Credit Corporation',
            reCmtyBank: 'Community Bank',
            reCoreBank: 'Core Bank',
            reCornerstone: 'Cornerstone Bank',
            reCornhusker: 'Cornhusker Bank',
            reCrestar: 'Crestar Mortgage Corporation',
            reCrossCountry: 'CrossCountry Mortgage Inc',
            reCrossFirst: 'CrossFirst Bank',
            reDaleFCU: 'Dale Employees Federal Credit Union',
            reDeutsche: 'Deutsche Bank National Trust Company',
            reDiscover: 'Discover Bank',
            reDLJ: 'DLJ Mortgage Capital Inc',
            reDundee: 'Dundee Bank',
            reEVBT: 'Elkhorn Valley Bank & Trust Company',
            reEmbrace: 'Embrace Home Loans Inc',
            reEnterprise: 'Enterprise Bank',
            reEquitable: 'Equitable Bank',
            reExchBT: 'Exchange Bank & Trust',
            reExchGib: 'Exchange Bank of Gibbon',
            reExchange: 'Exchange Bank',
            reFM: 'F & M Bank',
            reFCLSC: 'Farm Credit Leasing Services Corporation',
            reFCSA: 'Farm Credit Services of America',
            reFCSM: 'Farm Credit Services of the Midlands',
            reFSA: 'Farm Service Agency',
            reFarmers: 'Farmers State Bank',
            reFedTopeka: 'Federal Home Loan Bank of Topeka',
            reFedMort: 'Federal Home Loan Mortgage Corporation',
            reFannieMae: 'Federal National Mortgage Assn',
            reFidelity: 'Fidelity National Title Insurance Company',
            reFieldstone: 'Fieldstone Mortgage Company',
            re5th3rd: 'Fifth Third Bank',
            reFirstAmerSvgs: 'First American Savings Bank',
            reFATIC: 'First American Title Insurance Company',
            reFirstBancroft: 'First Bank of Bancroft',
            reFirstUtica: 'First Bank of Utica',
            reFirstCmty: 'First Community Bank',
            reFirstDak: 'First Dakota National Bank',
            reFirstMagnus: 'First Magnus Financial Corp',
            reFirstKey: 'Firstkey Mortgage LLC',
            reFirstMidwest: 'First Midwest Bank',
            reFirstMort: 'First Mortgage Company LLC dba Equitable Mortgage of Nebraska',
            reFirstNebr: 'First Nebraska Bank',
            re1nbt: 'First National Bank & Trust Company',
            re1nbne: 'First National Bank NE',
            refnbo: 'First National Bank of Omaha',
            re1nbFairbury: 'First National Bank Fairbury',
            re1nCU: 'First Nebraska Credit Union',
            re1neCU: 'First Nebraska Educators Credit Union',
            re1nenebr: 'First Northeast Bank of Nebraska',
            re1Premier: 'First Premier Bank',
            re1sbt: 'First State Bank & Trust Company',
            re1sbNebr: 'First State Bank of Nebraska',
            re1sb: 'First State Bank',
            reFirstTri: 'First Tri-County Bank',
            reFirstWestroads: 'First Westroads Bank',
            reFirstBank: 'FirstBank of Nebraska',
            reFivePts: 'Five Points Bank',
            reFlagstar: 'Flagstar Bank',
            reFortress: 'Fortress Credit Company LLC',
            reFoundationOne: 'Foundation One Bank',
            re4pts: 'Four Points Federal Credit Union',
            reFranklin: 'Franklin American Mortgage Company',
            reFreedom: 'Freedom Mortgage Corp',
            reFrontier: 'Frontier Bank',
            reGateway: 'Gateway Mortgage Group LLC',
            reGenerations: 'Generations Bank',
            reGreatPlains: 'Great Plains State Bank',
            reGSB: 'Great Southern Bank',
            reGWB: 'Great Western Bank',
            reHeartland: 'Heartland Bank',
            reHenderson: 'Henderson State Bank',
            reHeritage: 'Heritage Bank',
            reHFSL: 'Home Federal Savings & Loan Assn',
            reHomeLoan: 'Home Loan Investment Bank',
            reHomestead: 'Homestead Bank',
            reHorizon: 'Horizon Bank',
            reHSBC: 'HSBC Bank',
            reIowaBankMort: 'Iowa Bankers Mortgage Corp',
            reJeffCo: 'Jefferson County Bank',
            reJones: 'Jones National Bank & Trust Company',
            reJPMorgan: 'JPMorgan Chase Bank',
            reJPMorganMort: 'JPMorgan Mortgage Acquisition Corp',
            reLakeview: 'Lakeview Loan Servicing LLC',
            reLiberty: 'Liberty First Credit Union',
            reLincolnFSB: 'Lincoln FSB of Nebraska',
            reLoanDepot: 'LoanDepot.com LLC',
            reLocher: 'US Bank',
            reMalvern: 'Malvern Bank',
            reMCB: 'Madison County Bank',
            reMember: 'Members Mortgage Services LLC',
            reMembersOwn: 'MembersOwn Credit Union',
            reMERS: 'MERS',
            reMetro: 'Metro Credit Union Mortgage',
            reMetroLife: 'Metropolitan Life Insurance Company',
            reMidAmer: 'Mid America Mortgage Inc',
            reMidwest: 'Midwest Bank',
            reMoria: 'Moria Development Inc dba Peoples Mortgage',
            reMtgRes: 'Mortgage Reseach Center LLC dba Veterans Home Loans',
            reMtgSpec: 'Mortgage Specialists LLC',
            reMut1FCU: 'Mutual First Federal Credit Union',
            reMutOmaha: 'Mutual of Omaha Bank',
            reNAFCO: 'NAFCO NE Federal Credit Union nka SAC Federal Credit Union',
            reNavy: 'Navy Federal Credit Union',
            reNationstar: 'Nationstar Mortgage LLC',
            reNebrComm: 'Nebraska Bank of Commerce',
            reNebrEnergyFCU: 'Nebraska Energy Federal Credit Union',
            reNIFA: 'Nebraska Investment Finance Authority',
            reNebrEDC: 'Nebraska Economic Development Corp',
            reNebrStBk: 'Nebraska State Bank of Omaha',
            reNewPenn: 'New Penn Financial LLC dba Shellpoint Mortgage Servicing',
            reNewRes: 'New Residential Mortgage LLC',
            reNASB: 'North American Savings Bank',
            reNENebrFCU: 'Northeast Nebraska Federal Credit Union',
            reNWBk: 'Northwest Bank',
            reOakCrk: 'Oak Creek Valley Bank',
            reOcwen: 'Ocwen Loan Servicing LLC',
            reOldRep: 'Old Republic National Title Insurance Company',
            reOmahaFCU: 'Omaha Federal Credit Union',
            reParamount: 'Paramount Residential Mortgage Group Inc',
            rePathway: 'Pathway Bank',
            rePennyMac: 'PennyMac Loan Services LLC',
            rePinnBank: 'Pinnacle Bank',
            rePVB: 'Platte Valley Bank',
            rePNC: 'PNC Bank',
            rePNCMort: 'PNC Mortgage',
            rePrivateMtg: 'The Private Mortgage Group LLC',
            rePremier: 'Premier Bank',
            rePremierHome: 'Premier Home Mortgage',
            rePremierLending: 'Premier Lending Alliance LLC',
            rePrincipalResMtg: 'Principal Residential Mortgage Inc',
            reQuicken: 'Quicken Loans Inc',
            reRegent: 'Regent Financial Group',
            reReverse: 'Reverse Mortgage Solutions Inc',
            reSAC: 'SAC Federal Credit Union',
            reSantander: 'Santander Bank',
            reSecBk: 'Security Bank',
            reSec1Bk: 'Security First Bank',
            reSecHome: 'Security Home Bank',
            reSecNatl: 'Security National Bank',
            reSecState: 'Security State Bank',
            reSilk: 'Silk Abstract Company',
            reSirva: 'Sirva Mortgage Inc',
            reSBA: 'Small Business Administration',
            reSpecLoan: 'Specialized Loan Servicing LLC',
            reSpiritAmer: 'Spirit of America Federal Credit Union',
            reStanton: 'Stanton State Bank',
            reStewart: 'Stewart Title Guaranty Company',
            reColon: 'State Bank of Colon',
            reStateFarm: 'State Farm Bank',
            reStateNebr: 'State Nebraska Bank',
            reSuntrust: 'Suntrust Mortgage Inc',
            reTIAA: 'TIAA FSB dba EverBank',
            reTierOne: 'TierOne Bank',
            reTilden: 'Tilden Bank',
            re2rb: 'Two Rivers Bank',
            reUSAA: 'USAA Federal Savings Bank',
            reUSBank: 'US Bank',
            reUBT: 'Union Bank & Trust Company',
            reUnitedFidelity: 'United Fidelity Funding Corp',
            reUnitedRep: 'United Republic Bank',
            reUSHome: 'US Home Mortgage Inc',
            reValley: 'Valley Bank & Trust',
            reVeridian: 'Veridian Credit Union',
            reWSB: 'Wahoo State Bank',
            reWCB: 'Washington County Bank',
            reWaypoint: 'Waypoint Bank',
            reWFB: 'Wells Fargo Bank',
            reWFF: 'Wells Fargo Financial',
            reWestgate: 'Westgate Bank',
            reWestern: 'Western National Bank',
            reWilmington: 'Wilmington Savings Fund Society',
            reWyndham: 'Wyndham Capital Mortgage Inc',
            reYork: 'York State Bank'
        }

        # This is where the actual fix and restoration of the list starts
        mylist = []
        for name in namelist:  # namelist is passed as a parameter into this function
            # Initialize and define object
            myname = WhatAmI(name)
            # start checking if name is a bank
            for key in mybank:
                try:
                    if key.search(name) is not None:
                        myname = WhatAmI(name, True)
                except:
                    continue
            # end checking if name is a bank
            # start checking if name is a business
            # TODO see if a regex is on internet to determine if a name is a business
            mybusiness = [reChurch, reCompany, reCorp, reFarms, reInc, reLLC, reLTD, rePC]
            if not myname.isbank:
                for business in mybusiness:
                    try:
                        if business.search(name) is not None:
                            myname = WhatAmI(name, False, True)
                    except:
                        continue
            # end checking if name is a business
            mylist.append(myname)

        # this line keeps me from having duplicate values but maintains the order of the list
        d = list(OrderedDict.fromkeys(mylist))

        self.name = d
        return self.name

    def get_name(self):
        ''' This method must be called from the program and it should contain an index of the list
        item you want to get, otherwise it will return the entire list.'''
        myname = self.fix_name(self.name)
        self.name = myname
        return self.name

    def set_name(self, name, index):
        self.name[index] = name[index]


class WhatAmI(BuyerSeller):
    def __init__(self, name, isbank=False, isbusiness=False, istrust=False, isestate=False):
        BuyerSeller.__init__(self, name)
        self.isbank = isbank
        self.isbusiness = isbusiness
        self.istrust = istrust
        self.isestate = isestate

    def get_isbank(self):
        return self.isbank

    def get_isbusiness(self):
        return self.isbusiness

    def get_isestate(self):
        return self.isestate

    def get_istrust(self):
        return self.istrust

    def __set_isbank(self, status):
        self.isbank = status

    def __set_isbusiness(self, status):
        self.isbusiness = status

    def __set_isestate(self, status):
        self.isestate = status

    def __set_istrust(self, status):
        self.istrust = status

    def __iter__(self):
        self.n = 0
        return self

    def __len__(self):
        return len(self.name)

    def __next__(self):
        if self.n <= len(self.name) - 1:
            thisname = self.name[self.n]
            self.n += 1
            return thisname
        else:
            raise StopIteration

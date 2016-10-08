from random import randint;

exp_cnt = 10000;
coin_cnt = 1000;
toss_cnt = 10;
debug = True;

def ExpResult():
    def __init__(self):
        self.c_1 = None;
        self.c_rand= None;
        self.c_min= None;
        self.c_list = [];
    def setC_rand(self):
        self.c_rand = self.c_list[rand_int(0, len(rand_int)-1)];
        print "setting c_rand to: " + str(c_rand);

def run_cointoss(c_cnt, dbug):
    tmp_rst = ExpResult();
    return tmp_rst
    
    
results = [];
e_cnt = 0;

while e_cnt < exp_cnt:
    tmp_rst = run_cointoss(coin_cnt, debug);
    results.append(tmp_rst);
    e_cnt += 1;
from __future__ import division;
from random import randint, uniform;

exp_cnt = 10000;
coin_cnt = 1000;
toss_cnt = 10;
debug = False;

class ExpResult():
    def __init__(self):
        self.c_1 = None;
        self.c_rand= None;
        self.c_min= None;
#       c_list is a list of probability of head for each coin  
        self.c_list = [];
    def setC_rand(self):
        self.c_rand = self.c_list[randint(0, len(self.c_list)-1)];
        if debug: print "setting c_rand to: " + str(self.c_rand);
    def setC_1(self):
        self.c_1 = self.c_list[0];
        if debug: print "setting c_1 to: " + str(self.c_1);
    def setC_min(self, c_cnt, v_min):
        self.c_min = (c_cnt, v_min);
        if debug: print "setting c_min to: " + str(self.c_min);

def run_cointoss(c_cnt, t_cnt, dbug):
    tmp_rst = ExpResult();
    c_min = 0;
    v_min = 1;
    for i in range(c_cnt):
                
        head_cnt = 0;
        for j in range(t_cnt):
            tmp_rand =uniform(0, 1);
#             if dbug: print tmp_rand;
            if (tmp_rand > 0.5):
                head_cnt+= 1;
            else:
                None;
        tmp_v = head_cnt/t_cnt;
        if dbug: print tmp_v;
        
        v_min = tmp_v if tmp_v < v_min else v_min;
        c_min = i if tmp_v < v_min else c_min;
        
        tmp_rst.c_list.append((i,tmp_v));
    
    tmp_rst.setC_rand();
    tmp_rst.setC_1();
    tmp_rst.setC_min(c_min, v_min);
    
    return tmp_rst
    
    
if debug: results = [];
e_cnt = 0;
v_1_tot = 0;
v_min_tot = 0;
v_rand_tot = 0;

while e_cnt < exp_cnt:
    tmp_rst=run_cointoss(coin_cnt, toss_cnt, debug);
    if debug: results.append(tmp_rst);
    v_1_tot += tmp_rst.c_1[1];
    v_min_tot += tmp_rst.c_min[1];
    v_rand_tot += tmp_rst.c_rand[1];
    e_cnt += 1;
    
print "v_1 avg: " + str(v_1_tot/e_cnt) + " v_min avg: " + str(v_min_tot/e_cnt) + " v_rand avg: " + str(v_rand_tot/e_cnt);
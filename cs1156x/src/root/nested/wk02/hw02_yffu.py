from __future__ import division;
from random import randint, uniform;
from root.nested.wk01.hw01_yffu import get_initln, get_datapts, get_mismat, update_cls, get_y, dot_type, write_csv;
from numpy.linalg import inv;
import numpy as np;
import matplotlib.pyplot as plt;

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

def get_pseudoinv(my_x):
    mat_x = np.matrix(my_x);
    mat_xt = mat_x.transpose();
    return inv(mat_xt * mat_x)*mat_xt;

def get_linreg_w(my_x, my_y):
    pseudo = get_pseudoinv(my_x);
    mat_y = [my_y[x] for x in my_x];
    mat_y = np.matrix(mat_y).transpose();
    if debug: print "multiplying pseudo inv : " + str(pseudo) + " with y matrix: " + str(mat_y);
    return np.dot(pseudo,mat_y);

def plot_ln(my_w, my_flx, clr):
    my_fly = [ get_y(x, my_w) for x in my_flx]; 
    plt.plot(my_flx, my_fly, clr, linewidth = 2);        
        
    plt.axis([-1.2,1.2,-1.2,1.2]);
    plt.axhline(linewidth=1, color='blue');
    plt.axvline(linewidth=1, color='blue');
    
def plot_pts(my_x, my_cls1, my_cls2 = None):
    if my_cls2 == None:
        for tmp_x in my_x:
            plt.plot(tmp_x[0], tmp_x[1], dot_type(my_cls1[tmp_x], 1));
    else:
        for tmp_x in my_x:
            plt.plot(tmp_x[0], tmp_x[1], dot_type(my_cls1[tmp_x], my_cls2[tmp_x]));
            
def run_linreg(*args):
    
    num_d, save_img = args;
    
    my_w, my_f, my_flx, my_fly0 = get_initln(save_img);
    
    my_x, my_y, my_yw = get_datapts(num_d, my_f, my_w);
            
    my_w = get_linreg_w(my_x, my_y);
    
    my_yw = update_cls(my_x, my_w);
    
    if debug: 
        plot_pts(my_x, my_y, my_yw);
        
        plot_ln(my_w, my_flx, 'c--');
        
        plot_ln(my_f, my_flx, 'g--');
           
        plt.show();
        
    mismat_x, mismat_cnt = get_mismat(my_yw, my_y);
    
    mismat_prt = mismat_cnt/100.0;
    
    return my_w, mismat_prt;

def run_exp_coins(*args):
    exp_cnt, coin_cnt, toss_cnt = args;
    
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

def run_exp_linreg(*args):
    exp_cnt, num_dot = args;
    e_cnt = 0;
    prb_tot=0.0;
    rcd = [];

    while e_cnt < exp_cnt:
        tmp_w, mismat_prt = run_linreg(num_dot, False);
        tmp_w = tmp_w.transpose();
        prb_tot += mismat_prt; 
        e_cnt += 1;
        rcd.append([tmp_w, mismat_prt]);
        if debug: 
            print "weights for g as estimated by linreg: " + str(tmp_w);
            print "fraction of insample points classified incorrectly by g: " + str(mismat_prt); 
    
    write_csv(rcd, 'record_linreg.csv');
    prb_avg = prb_tot/exp_cnt;
    
    print "average fraction of mismatch on g: " + str(prb_avg);
        
# run_exp_coins(1000, 1000, 10);
# run_exp_pla(100, 10);
run_exp_linreg(1000, 100);
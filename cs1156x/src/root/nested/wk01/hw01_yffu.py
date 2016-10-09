'''
Created on Oct 9, 2013

@author: Yuan-Fang
'''

import random, time;
import matplotlib.pyplot as plt;
import numpy as np;
from numpy.linalg import inv;
from scipy.integrate import quad;
from random import randint;
import csv;
    
debug = False;
save_image = False;

#Todo - figure out what they mean by chose randomly. Perhaps change to have a shuffle.
def get_y(x, weight):
    # if condition for when y is zero.
    if weight.item(1,0) != 0:
        return -(weight.item(2, 0)+weight.item(0,0)*x)/ weight.item(1,0); 
    else:
        return 0;
    
def get_cls(x, w):
    return np.sign(np.mat(x) * w).item(0);

def get_mismat(tmp_yw, my_y):
    mismat_xs =[];
    for k in tmp_yw:
        if tmp_yw[k] != my_y[k]:
            mismat_xs.append(k);
    if len(mismat_xs) == 0:
        return None, len(mismat_xs);
    else:
        pt = mismat_xs[randint(0, len(mismat_xs)-1)];
        if debug: print "Mismatch at point: " + str(pt);
        return pt, len(mismat_xs);

def dot_type(yw, y):
    dot = None;
    if y*yw < 0:
        dot='ro';
    elif y*yw > 0:
        dot = 'go';
    else:
        dot = 'yo';
    return dot;

# calculate area for probability    
def line_val(x, weight):
    if weight.item(1,0) != 0:
        y= -(weight.item(2, 0)+weight.item(0,0)*x)/ weight.item(1,0);
        if y > 1: return 1;
        elif y < -1 : return -1;
        else: return y; 
    else: return 0;
    
def line_diff(x, wgt1, wgt2):
    return line_val(x, wgt1) - line_val(x, wgt2);

def write_csv(data, pathname):
    file = open(pathname, 'wb')
    writer = csv.writer(file);
    writer.writerows(data);
    file.close();
    
def get_datapts(num_d, my_f, my_w):
    my_x = [];
    my_y = dict();
    my_yw = dict();
    for i in range(0, num_d):
        tmp_x = (random.uniform(-1, 1), random.uniform(-1, 1), 1);
        my_x.append(tmp_x);
        
        tmp_y = get_cls(tmp_x, my_f);
        my_y[tmp_x]=tmp_y;
        
        tmp_yw = get_cls(tmp_x, my_w);
        my_yw[tmp_x] = tmp_yw;
            
        if debug:
            plt.plot(tmp_x[0], tmp_x[1], dot_type(tmp_y, 1)); 
    return my_x, my_y, my_yw;

def update_cls(my_x, my_w):
    my_yw = dict();
    for tmp_x in my_x:
        tmp_yw = get_cls(tmp_x, my_w);
        my_yw[tmp_x]=tmp_yw;
    return my_yw;

def get_initln(save_img):
    my_w = np.transpose(np.mat([0,0,0]));
    
    my_fp = [];
    my_fp.append((random.uniform(-1, 1), random.uniform(-1, 1)));
    my_fp.append((random.uniform(-1, 1), random.uniform(-1, 1)));
    
    my_c = np.mat([[1], [1]]);
    my_f = inv(my_fp) * my_c;
    
    my_f = np.concatenate((my_f, np.mat([-1])), axis = 0);
    #below for validating linear function produced matches initial points generated.
    my_flx = np.arange(-1.2,1.3, 0.1);
    my_fly0 = [ get_y(x, my_f) for x in my_flx];
    
    if debug or save_img:
        print my_w;
        print my_f;
        
        print my_f.item(0,0);
        print my_f.item(1,0); 
         
        plt.plot(my_flx, my_fly0, 'r--')
        
    # end validation
    return my_w, my_f, my_flx, my_fly0;
    
# main section, to be called in loop at bottom
def run_perceptron(num_d, save_img):
    
    my_w, my_f, my_flx, my_fly0 = get_initln(save_img);
    
    my_x, my_y, my_yw = get_datapts(num_d, my_f, my_w);
            
    mismat_x, mismat_cnt = get_mismat(my_yw, my_y);
    
    if debug:
        
        print "number of mismatches: " + mismat_cnt;
        my_fly = [ get_y(x, my_w) for x in my_flx]; 
        
        plt.plot(my_flx, my_fly, 'c--', linewidth = 2);        
        
        plt.axis([-1,1,-1,1]);
        plt.axhline(linewidth=1, color='blue');
        plt.axvline(linewidth=1, color='blue');
        
        plt.plot(mismat_x[0], mismat_x[1], 'yo');
        plt.show();
    
    itr_ctr = 0;
    
    while mismat_x != None:
        # update my_w
        
        my_w = my_w + my_y[mismat_x]*np.transpose(np.mat(mismat_x));
        
        pt_ctr = 0;
        
        for k in my_y:
            # update each value for my_yw
            tmp_yw = get_cls(k, my_w);
            my_yw[k] = tmp_yw;
                
            if debug:
                plt.plot(k[0], k[1], dot_type(tmp_yw, my_y[k]));
                print "iteration " + str(itr_ctr) + " point # " + str(pt_ctr) + " at " + str(k);
                print "predicted " + str(tmp_yw) + " versus actual " + str(my_y[k]);
                
            pt_ctr +=1;
        
        # check for mismatch in updated my_yw and update mismat_x
        mismat_x, mismat_cnt = get_mismat(my_yw, my_y);
        
        if debug or save_img:
            my_fly = [ get_y(x, my_w) for x in my_flx]; 
            
            plt.axis([-1,1,-1,1]);
            plt.axhline(linewidth=1, color='blue');
            plt.axvline(linewidth=1, color='blue');
            plt.plot(my_flx, my_fly, 'c--', linewidth = 1); 
            plt.plot(my_flx, my_fly0, 'r--', linewidth = 1);
            
            if mismat_x: plt.plot(mismat_x[0], mismat_x[1], 'yo');
            print "number of mismatches: " + mismat_cnt;
            print "new w: "; 
            print my_w;
            if not save_img: plt.show();
            
        itr_ctr += 1;
    
    if save_img:
        plt.savefig('plot.png');
#     calculate summary on exit loop    
    prb, err = quad(line_diff, -1, 1, args = (my_f, my_w)); 
    prb = np.abs(prb) /4; 
    
    return [itr_ctr, prb]

def run_exp_pla(*args):

    num_hyp, num_dot = args;
    
    itr_hyp = 0;
    ctr_tot=0;
    prb_tot=0;
    rcd = [];
    
    while itr_hyp < num_hyp:
        ctr, prb = run_perceptron(num_dot, save_image);
        ctr_tot += ctr;
        prb_tot += prb;
        itr_hyp += 1;
        rcd.append([ctr, prb]);
        if debug: print "found solution on iteration: " + str(ctr) + " with probability of mismatch: " + str(prb);
    
    write_csv(rcd, 'record.csv');
    prb_avg = prb_tot/num_hyp;
    ctr_avg = ctr_tot/num_hyp;
    
    print "average iterations: " + str(ctr_avg) + " average probability: " + str(prb_avg);
    
# run_exp_pla(100, 10);
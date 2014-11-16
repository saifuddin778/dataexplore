from __future__ import division
import sys
import os
import math
import json
import webbrowser


class dataexplore(object):
    """
    main object -- generates the key insights related to dataset.
    Call this with the required dataset value.
    """
    def __init__(self, data, name=False):
        self.data = data
        self.t_data = zip(*self.data)
        self.constant_length = len(self.data)
        self.features = {}
        self.features['n_features'] = len(self.t_data)
        self.features['feature_details'] = dict([('f'+str(_+1), {}) for _ in range(0, len(self.t_data))])
        self.features['correlations'] = {}
        self.features['histograms'] = {}
        self.features['scatter_points'] = {}
        self.basic_features()
        self.pairwise_correlation()
        self.gen_histograms()
        if not name:
            self.dataset_name = 'dataexplore'
        else:
            self.dataset_name = name
        self.save_to_file()
        self.generate_html()
        self.display_report()
        

    def basic_features(self):
        """calculate all the means, standard deviations, ranges, and variances"""
        for i in xrange(0, len(self.t_data)):
            current_ = self.t_data[i]
            label_ = 'f'+str(i+1)
            mean_ = sum(current_)/len(current_)
            self.features['feature_details'][label_]['mean'] = round(mean_, 3)
            self.features['feature_details'][label_]['std'] = round(math.sqrt(sum([math.pow((i - mean_), 2) for i in current_])/(len(self.data)-1)), 3)
            self.features['feature_details'][label_]['max'] = round(max(current_), 3)
            self.features['feature_details'][label_]['min'] = round(min(current_), 3)
            
    def get_combinations(self):
        """generates n(n-1)/2 combinations based on the n features"""
        unique_labels = [a for a in range(0, len(self.t_data))]
        g = []
        for i, a in enumerate(unique_labels):
            current_ = unique_labels[i]
            for e, b in enumerate(unique_labels):
                if e > i:
                    g.append((unique_labels[i], unique_labels[e]))
        return g

    def pearson_correlation_coefficient(self, fx, fy):
        """Returns the pearson correlation coefficient between two variables"""
        label_fx, label_fy = 'f'+str(fx+1), 'f'+str(fy+1)
        mean_fx, mean_fy = self.features['feature_details'][label_fx]['mean'], self.features['feature_details'][label_fy]['mean']
        cov_fx_fy = sum((fxi - mean_fx)*(fyi - mean_fy) for fxi, fyi in zip(self.t_data[fx], self.t_data[fy]))/(self.constant_length-1)
        divisor = (self.features['feature_details'][label_fx]['std']*self.features['feature_details'][label_fy]['std'])
        return round(cov_fx_fy/divisor, 3)
    
    def histogram(self, f):
        """Returns the histogram for the given array"""
        hist = {}
        for i in xrange(0, len(f)):
            v = round(float(f[i]), 1)
            if v in hist:
                hist[v] += 1
            else:
                hist[v] = 1
        return hist
    
    def pairwise_correlation(self):
        """generates pairwise correltation scores"""
        combinations = self.get_combinations()
        for a,b in combinations:
            label_a, label_b = 'f'+str(a+1), 'f'+str(b+1)
            self.features['correlations'][label_a+','+label_b] = self.pearson_correlation_coefficient(a,b)
            self.features['scatter_points'][label_a+','+label_b] = self.get_scatter_points(a,b)
            #print len(self.t_data[a]), len(self.t_data[b])
    
    def gen_histograms(self):
        """generates the histogram for each feature"""
        for i in xrange(0, len(self.t_data)):
            current_ = self.t_data[i]
            label_ = 'f'+str(i+1)
            self.features['histograms'][label_] = self.histogram(self.t_data[i])

    def get_scatter_points(self, a,b):
        e = []
        if len(self.t_data[a]) > 1000:
            v = int(len(self.t_data[a])/1000)
            for i in range(0, len(self.t_data[a])):
                if not i % v:
                    e.append((self.t_data[a][i], self.t_data[b][i]))
        else:
            for i in range(0, len(self.t_data[a])):
                e.append((self.t_data[a][i], self.t_data[b][i]))

        return e
                
    
    def save_to_file(self):
        self.file_name = 'dataexplore_reports/'+self.dataset_name+'.js'
        var_name = 'var explorer'
        f = open(self.file_name, 'wb')
        f.write(var_name + ' = ' + json.dumps(self.features) +';')
        f.close()
    
    def get_template(self, name):
        location = 'templates'
        f = open(location+'/'+name, 'rb')
        return f.read().split('\n')
    
    def generate_html(self):
        templates = {'default': 'default_template.html'}
        html_construct = self.get_template(templates['default'])
        script_name = "<script src='../"+self.file_name+"'></script>"
        html_construct.insert(2, script_name)
        html_construct = ''.join(html_construct)
        out_file = 'dataexplore_presentations/'+self.dataset_name+'.html'
        f = open(out_file, 'w')
        f.write(html_construct)
        f.close()
    
    def display_report(self):
        url_ = 'file://'+os.path.dirname(os.path.abspath('__file__'))+'/dataexplore_presentations/'+self.dataset_name+'.html'
        webbrowser.open(url_, 2)


import os
import numpy as np
from process_outputs import process_outputs

dbpath= "databases/data/db/outputs"
formats= ['src-tar','src-tar-port','src','src-port','tar','tar-port']
mining_minsup_only = ['CM-SPADE','CM-ClaSP','VGEN', 'VMSP']
mining_timewindow = ['HirateYamana', 'Fournier08-Closed+time']
mining_rules = ['RuleGrowth','TRuleGrowth']
mining_top_k = ['TKS','TopSeqRules']

def make_dir(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

def mining(methods,min_sup):
    full = dbpath + '/full'
    _0025percentage = dbpath + '/2.5percentage/basic/'
    for mining_method in methods:
        make_dir('./mining_outputs/' + mining_method +'/mining_raw/1.txt')
        make_dir('./mining_outputs/' + mining_method +'/statistics/1.txt')
        dir_out = './mining_outputs/' + mining_method
        for _format in formats:
            print("[+] Current processing.... \n")
            print("[+] Method: " + mining_method)
            print("[+] Format: "+ _format)
            print("[+] Minimal support value: " + str(min_sup))
            input_dir = _0025percentage + _format
            output_file = dir_out + '/mining_raw/' + _format + str(min_sup) + ".txt"
            result_file = dir_out + '/statistics/' + _format + str(min_sup) + ".stats"
            if 'HirateYamana' in methods:
                os.system('java -jar ../spmf.jar run %s %s %s %s 0 2 0 2 >> %s'%(mining_method,input_dir,output_file,str(min_sup),result_file))
            if (mining_method=='RuleGrowth'):
                os.system('java -jar ../spmf.jar run %s %s %s %s 0.5 >> %s'%(mining_method,input_dir,output_file,str(min_sup),result_file))
            if (mining_method=='TRuleGrowth'):
                os.system('java -jar ../spmf.jar run %s %s %s %s 0.5 3 >> %s'%(mining_method,input_dir,output_file,str(min_sup),result_file))
            else:
                os.system('java -jar ../spmf.jar run %s %s %s %s >> %s'%(mining_method,input_dir,output_file,str(min_sup),result_file))

def main():
    #Default support value = 10%
    # CM-SPADE with 1 options minsup
    # os.system('java -jar ../spmf.jar run CM-SPADE %s %s %s > '%(input_dir,ouput_dir,str(min_sup),result_file))
    # process_outputs(args.database, args.output_file, percentage_support=not args.no_support, precision=args.precision)
    for min_sup in np.arange(0.1,0.5,0.1):
        mining(mining_minsup_only,min_sup)
        # mining(mining_timewindow, min_sup)
    for k in range(1,20,1):
        mining(mining_top_k, k)

if __name__ == '__main__':
    main()
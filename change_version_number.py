import os 

files = os.listdir('.')

for filename in files:
    if filename[-3:] == '.py':
        print filename
        os.system('cp %s %s'%(filename, filename+'old'))
        with open(filename) as fid:
            content=fid.read()
        if 'giovanni.iadarola@cern.ch' in content:
            content=content.replace('PyECLOUD Version 4.23 nonconvex test', 'PyECLOUD Version 4.23 nonconvex test nonconvex test')
            with open(filename,'w') as fid:
                fid.write(content)
        
os.system('rm *.pyold')

from PyECLOUD.buildup_simulation import BuildupSimulation

sim_input_folder = '../../testing/tests_buildup/LHC_ArcDipReal_450GeV_sey1.70_2.5e11ppb_bl_1.00ns'

t_stop_list = [5e-9, 25e-9, 123e-9, 25e-9, 250e-9, 500e-9, None]

sim = BuildupSimulation(pyecl_input_folder=sim_input_folder, 
        filen_main_outp='./Pyecltest.mat',
        extract_sey=False)

for ii, t_stop in enumerate(t_stop_list):
    print('\n\n==============================')
    print('Simulation run %d - t_stop = %s s'%(ii, repr(t_stop))) 
    print(' starting at tt=%s s'%repr(sim.beamtim.tt_curr)) 
    
    sim.run(t_end_sim = t_stop)
    
    print(' after run a tt=%s'%repr(sim.beamtim.tt_curr))

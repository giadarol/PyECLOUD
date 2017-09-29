import shutil
import os

all_sim_folders = [
    # 'LHC_ArcDipReal_450GeV_sey1.00_2.5e11ppb_bl_1.00ns_gas_ionization',
    # 'LHC_ArcDipReal_450GeV_sey1.70_2.5e11ppb_bl_1.00ns',
    # 'LHC_ArcDipReal_450GeV_sey1.70_2.5e11ppb_bl_1.00ns_change_s_and_E0',
    # 'LHC_ArcDipReal_450GeV_sey1.70_2.5e11ppb_bl_1.00ns_multigrid',
    # 'LHC_ArcQuadReal_450GeV_sey1.65_2.5e11ppb_bl_1.00ns',
    # 'LHC_ArcQuadReal_450GeV_sey1.65_2.5e11ppb_bl_1.00ns_circular',
    # 'LHC_ArcQuadReal_450GeV_sey1.65_2.5e11ppb_bl_1.00ns_skew',
    # 'LHC_ArcQuadReal_450GeV_sey1.65_2.5e11ppb_bl_1.00ns_skew_circular',
    # 'LHC_Sextupole_450GeV_sey1.65_2.5e11ppb_bl_1.00ns',
    # 'LHC_Sextupole_450GeV_sey1.65_2.5e11ppb_bl_1.00ns_skew',
    # 'CLIC_DRe-_Drift_0.5ns_4.0e9ppb_gas_ionization_ecloud_sey2.0',
    # 'CLIC_DRe+_Drift_0.5ns_4.0e9ppb_gas_ionization_ecloud_sey2.0',
    # 'CLIC_DRe-_Drift_0.5ns_4.0e9ppb_gas_ionization_ions_A18',
    # 'CLIC_DRe+_Drift_0.5ns_4.0e9ppb_gas_ionization_ions_A18',
]

for folder in all_sim_folders:
    for dim in [3]:
        ref_file = folder + '/Pyecltest_angle%iD_ref.mat' % dim
        mat_file = folder + '/Pyecltest_angle%iD.mat' % dim
        if os.path.isfile(ref_file):
            os.remove(ref_file)
        shutil.copy(mat_file, ref_file)
        print('%s replaced by %s' % (ref_file, mat_file))


#for folder in all_sim_folders:
#    ref_file = folder + '/Pyecltest_ref.mat'
#    new_ref_file = folder + '/Pyecltest_3D_ref.mat'
#    ref_file_2D = './old_tests_cosine_2D/' + ref_file
#    new_ref_file_2D = folder + 'Pyecltest_2D_ref.mat'
#    shutil.move(ref_file, new_ref_file)
#    shutil.copy(ref_file_2D, new_ref_file_2D)
#    print('%s replaced by %s' % (ref_file, new_ref_file))
#    print('%s replaced by %s' % (ref_file_2D, new_ref_file_2D))

#for folder in all_sim_folders:
#    new_ref_file = folder + 'Pyecltest_3D_ref.mat'
#    ref_file = folder + '/Pyecltest_3D_ref.mat'
#    new_ref_file_2D = folder + 'Pyecltest_2D_ref.mat'
#    ref_file_2D = folder + '/Pyecltest_2D_ref.mat'
#    shutil.move(new_ref_file, ref_file)
#    shutil.move(new_ref_file_2D, ref_file_2D)

#for folder in all_sim_folders:
#    old_mat = folder +'/Pyecltest_3D_ref.mat'
#    new_mat = folder +'/Pyecltest_angle3D_ref.mat'
#    shutil.move(old_mat, new_mat)

import numpy as np
import matplotlib.pyplot as plt
import sec_emission_model_ECLOUD as ECL
import sec_emission_model_furman_pivi as fp
import mystyle as ms
from scipy.constants import e as qe

plt.close('all')
ms.mystyle(12)
linewid = 2

me = 9.10938356e-31
sey_mod = fp.SEY_model_FP_Cu(E_th=35., secondary_angle_distribution='cosine_3D',
                             switch_no_increase_energy=0, thresh_low_energy=-1)  # 276.8, 1.8848)
# sey_mod = ECL.SEY_model_ECLOUD(Emax=332., del_max=1.8848, R0=0.7, E_th=35., mufit=1.6636, secondary_angle_distribution='cosine_3D',
#                                sigmafit=1.0828, switch_no_increase_energy=0, thresh_low_energy=-1)


def extract_energy_distributions(n_rep, E_impact_eV_test, cos_theta_test, charge, mass):
    dists = {}
    for etype in sey_mod.event_types.keys():
        etype_name = sey_mod.event_types[etype]
        dists[etype_name] = []
    print('Extracting energy distributions...')
    for i_ct, ct in enumerate(cos_theta_test):
        print('%d/%d' % (i_ct + 1, len(cos_theta_test)))
        Ene = E_impact_eV_test
        nel_impact = np.ones(n_rep)
        # Assuming normal is along x
        v_mod = np.sqrt(2 * Ene * qe / mass) * np.ones_like(nel_impact)
        vx = v_mod * ct
        vy = v_mod * np.sqrt(1 - ct * ct)

        nel_emit_tot_events, event_type, event_info,\
            nel_replace, x_replace, y_replace, z_replace, vx_replace, vy_replace, vz_replace, i_seg_replace,\
            nel_new_MPs, x_new_MPs, y_new_MPs, z_new_MPs, vx_new_MPs, vy_new_MPs, vz_new_MPs, i_seg_new_MPs =\
            sey_mod.impacts_on_surface(
                mass=mass, nel_impact=nel_impact, x_impact=nel_impact * 0, y_impact=nel_impact * 0, z_impact=nel_impact * 0,
                vx_impact=vx * np.ones_like(nel_impact),
                vy_impact=vy * np.ones_like(nel_impact),
                vz_impact=nel_impact * 0,
                Norm_x=np.ones_like(nel_impact), Norm_y=np.zeros_like(nel_impact),
                i_found=np.int_(np.ones_like(nel_impact)),
                v_impact_n=vx * np.ones_like(nel_impact),
                E_impact_eV=Ene * np.ones_like(nel_impact),
                costheta_impact=ct * np.ones_like(nel_impact),
                nel_mp_th=1,
                flag_seg=True)

        v_replace_mod = np.sqrt(vx_replace**2 + vy_replace**2 + vz_replace**2)
        E_replace_eV = 0.5 * mass / qe * v_replace_mod * v_replace_mod

        v_new_MPs_mod = np.sqrt(vx_new_MPs**2 + vy_new_MPs**2 + vz_new_MPs**2)
        E_new_MPs_eV = 0.5 * mass / qe * v_new_MPs_mod * v_new_MPs_mod

        E_all_MPs_eV = np.concatenate([E_replace_eV, E_new_MPs_eV])

        for etype in sey_mod.event_types.keys():
            etype_name = sey_mod.event_types[etype]
            dists[etype_name].append(E_all_MPs_eV[event_type == etype])

    print('Done extracting energy distributions.')

    return dists


cos_theta_test = np.linspace(0, 1., 10) # np.array([1.]) #
E_0_single = 300
E_impact_eV_test = np.array([E_0_single] * int(1e5))
n_rep = 100000
alpha = 0.9

dists = extract_energy_distributions(n_rep, E_impact_eV_test, cos_theta_test, charge=qe, mass=me)

plt.close('all')
ms.mystyle_arial()

fig1 = plt.figure(1, figsize=(3 * 8, 2 * 8))
fig1.set_facecolor('w')
sp1 = fig1.add_subplot(2, 2, 1)
sp2 = fig1.add_subplot(2, 2, 2)
sp3 = fig1.add_subplot(2, 2, 3)
sp4 = fig1.add_subplot(2, 2, 4)
# sp5 = fig1.add_subplot(2, 3, 5)
# sp6 = fig1.add_subplot(2, 3, 6)

for i_ct, ct in enumerate(cos_theta_test):
    thiscol = ms.colorprog(i_ct, len(cos_theta_test))
    label = 'costheta=%.2f' % ct
    sp1.hist(dists['true'][i_ct], bins=60, color=thiscol, label=label, alpha=alpha, density=True)
    sp2.hist(dists['elast'][i_ct], bins=30, color=thiscol, label=label, alpha=alpha, density=True)
    sp3.hist(dists['rediff'][i_ct], bins=30, color=thiscol, label=label, alpha=alpha, density=True)
    sp4.hist(dists['absorb'][i_ct], bins=30, color=thiscol, label=label, alpha=alpha, density=True)
    # sp5.hist(dists['true'][i_ct] + dists['elast'][i_ct] + dists['rediff'][i_ct], color=thiscol, label=label)
    # sp6.hist(dists['true'][i_ct] + dists['elast'][i_ct], color=thiscol, label=label)

linewid = 3
sp2.plot(0, 0, 'k', label='Model PDF', linewidth=linewid)
sp2.legend(loc='best', prop={'size': 14})
sz = 24
sp1.set_ylabel('True secondaries', fontsize=sz)
sp2.set_ylabel('Elastic', fontsize=sz)
sp3.set_ylabel('Rediffused', fontsize=sz)
sp4.set_ylabel('Absorbed', fontsize=sz)
# sp5.set_ylabel('total')
# sp6.set_ylabel('true + elast')

# Compare with model
test_obj = fp.SEY_model_FP_Cu()
E_0 = np.array([E_0_single] * int(1e5))
energy = np.linspace(0.001, E_0_single, num=int(1e5))
# Rediffused
prob_density_r = test_obj.rediffused_energy_PDF(energy=energy, E_0=E_0)
sp3.plot(energy, prob_density_r, 'k', label='PDF', linewidth=linewid)
# Backscaterred
prob_density_e = test_obj.backscattered_energy_PDF(energy, E_0)
sp2.plot(energy, prob_density_e, 'k', label='PDF', linewidth=linewid)
# True secondaries
delta_ts = test_obj._delta_ts(E_0_single, 1)
prob_density_ts = test_obj.average_true_sec_energy_PDF(delta_ts=delta_ts, E_0=E_0_single, energy=energy)
sp1.plot(energy, prob_density_ts, 'k', label='PDF of true secondary electrons (average)', linewidth=linewid)

for sp in [sp1, sp2, sp3, sp4]:
    sp.grid('on')
    sp.set_xlabel('Electron energy [eV]')

plt.subplots_adjust(right=0.99, left=.06)


# test_obj = fp.SEY_model_FP_Cu()  # 276.8, 1.8848)

plt.suptitle('Energy distribution extraction tests: Furman-Pivi model', fontsize=30)

plt.show()
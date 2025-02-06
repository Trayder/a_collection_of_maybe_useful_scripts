
# select_by_alignment
#
# Author: Trayder Thomas
# Date  : 2024-08-13
#
import pymol

# example usage
# update_select_by_alignment("4wa9_B", "8ssn_A", ["tyr_all","lys_all"])

def update_select_by_alignment(ref, new_mol, sel_list=None):
    """
    PARAMS
      ref: reference object
      new_mol: object name, or [object,names] to be aligned
      sel_list: a list of selections to align and update

    CREATES (from select_by_alignment)
      aln: alignment object
      sel1: CA's of sel in ref 
      sel2: CA's matched by alignment in tgt

    NOTES
    When auto-building sel_list, cmd.get_names will pick
    every selection with any atom of ref
    """

    #if a list of selections is not provided update all selections that include ref
    if sel_list is None:
        sel_list = []
        for s in cmd.get_names('selections',0,ref):
            if s != 'sele':
                sel_list.append(s)
        
    if isinstance(new_mol, str):
        new_mol = [new_mol]
    
    for tgt in new_mol: 
        for upd_sel in sel_list:
            space = {'orig_resids': [],
                     'added_resids': [],
                     'new_resids': [],}
            trim_added = []
            cmd.select("tmp","(%"+upd_sel+" and "+ref+") and n. CA")
            n_res = cmd.iterate("%tmp", "orig_resids.append(resi)", space=space)
            # if not enough resids first try to add after last, then before first
            # only necessary if ref structure may be missing residues around upd_sel
            for i in range(3-n_res):
                base_res = space['orig_resids'][-1]
                try_res = str(int(base_res)+i+1)
                found_res = cmd.iterate(ref+" and n. CA and resi "+try_res, "added_resids.append(resi)", space=space)
                if found_res > 1:
                    print("error adding "+try_res+"("+base_res+"+"+str(i+1)+") to alignment")
                    break
                if found_res == 1:
                    trim_added.append(n_res)
                n_res += found_res
            for i in range(3-n_res):
                base_res = space['orig_resids'][0]
                try_res = str(int(base_res)-i-1)
                found_res = cmd.iterate(ref+" and n. CA and resi "+try_res, "added_resids.append(resi)", space=space)
                if found_res > 1:
                    print("error adding "+try_res+"("+base_res+"-"+str(-i-1)+") to alignment")
                    break 
                if found_res == 1:
                    trim_added.append(i)
                n_res += found_res
            if n_res < 3:
                print("could not expand alignment")
                continue
               
            align_resids = space['orig_resids'] + space['added_resids'] 

            align_sel = ref+" and (resi "+align_resids[0] 
            for resid in align_resids[1:]:
                align_sel += " or resi "+resid
            align_sel += ")"
            print(f"sel: {upd_sel}, orig: {space['orig_resids']}, added: {space['added_resids']}")

            select_by_alignment(ref, tgt, align_sel)
            if cmd.iterate("%all_align_sel and n. CA and "+tgt, "new_resids.append(resi)", space=space) == n_res:
                tgt_resids = []
                for i,resi in enumerate(space['new_resids']):
                    if i not in trim_added:
                        tgt_resids.append(resi)

                final_sel = tgt+" and %all_align_sel and (resi "+tgt_resids[0] 
                for resid in tgt_resids[1:]:
                    final_sel += " or resi "+resid
                final_sel += ")"
                cmd.select(upd_sel, final_sel, merge=1)
            else:
                print("residues lost in alignment of "+tgt)

    
cmd.extend("update_select_by_alignment", update_select_by_alignment)
print("A new function 'update_select_by_alignment' was added to PyMOL.")
print("Type 'help update_select_by_alignment' if you need help.")

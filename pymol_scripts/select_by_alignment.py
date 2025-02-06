
# select_by_alignment
#
# Author: Trayder Thomas
# Date  : 02-29-2024
#
import pymol

# example usage
# select_by_alignment("5k9i_A", "5u8l_A", "5k9i_A and i. 338-342"

def select_by_alignment(ref, targets, sel, debug=False):
    """
    PARAMS
      ref: reference object
      tgt: object name, or [object,names] to be aligned
      sel: sub-selection of ref to align to

    CREATES
      aln: alignment object
      sel1: CA's of sel in ref 
      sel2: CA's matched by alignment in tgt

    NOTES
    Remember you can expand to full residues using e.g.:
        `select alignres, br. alignsel`
    Because this is a sequence alignment, the only safe 
    choice is match residues by CA.
    Will fail if sel aligns with a gap
    If any residues align with a gap (show as colored
    in across from a gap in SeqView) it will offset the
    matching selection. So far I have not had this
    happen while using align(reset=1)
    Do not accidentally pass an alignment to ref or
    tgt or your computer will blow up
    """

    if isinstance(targets, str):
        targets = [targets]
    all_align_sel = None
    aln = "aln"

    for tgt in targets:
        print("aligning "+tgt)
        a1, a2, a_target = [],[],[]
        # space dictionary for iterate
        space = { 'a1' : a1, 
                  'a2' : a2,
                  'a_target' : a_target, 
                }
    
        # alignment, can't use cealign as no reset option
        # dunno what reset is meant to do, but it prevents alignment to gaps
        try:
            cmd.align(tgt, ref, cycles=0, object=aln, transform=0, reset=1)
        except:
            print("FAILED! alignment of "+tgt+" to "+ref)
            continue
    
        # record the initial indices
        s = "n. CA and (%s and %s)"
        cmd.iterate(s % (ref,aln), "a1.append(index)",space=space)
        cmd.iterate(s % (tgt,aln), "a2.append(index)",space=space)
    
        if debug:
            print("# [debug] num atom in aln1 = ", len(a1))
            print("# [debug] num atom in aln2 = ", len(a2))
    
        # focus the target selection
        cmd.iterate(sel + " and n. CA", "a_target.append(index)",space=space)
    
        if debug:
            print("# [debug] a_target has %d members." % len(a_target))
    
        id1, id2 = [], []
        for x in a_target:
            try:
                idx = a1.index(x)
                if debug:
                    print("Current index: %d" % idx)
                id1.append( str(a1[idx]) )
                id2.append( str(a2[idx]) )
            except:
                cmd.iterate(sel+" and n. CA and index "+str(x), 'print("WARNING! "+resn+resi+" not found in alignment")')
        
        if len(id2) <3:
            print("FAILED! Only "+str(len(id2))+" residues left for alignment")
            continue

        if debug: 
            print("# [debug] id1 = %s" % id1)
            print("# [debug] id2 = %s" % id2)
            
        sel1 = ref + " and index " + "+".join(id1)
        sel2 = tgt + " and index " + "+".join(id2)
        
        if debug:
            print("# [debug] sel1 = %s" % sel1)
            print("# [debug] sel2 = %s" % sel2)
    
        cmd.select("sel1", "br. "+sel1)
        cmd.select("sel2", "br. "+sel2)
        if all_align_sel is None:
            all_align_sel =  "(br. "+sel1+")"
        all_align_sel += " or (br. "+sel2+")" 
    cmd.select("all_align_sel", all_align_sel)

cmd.extend("select_by_alignment", select_by_alignment)
print("A new function 'select_by_alignment' was added to PyMOL.")
print("Type 'help select_by_alignment' if you need help.")

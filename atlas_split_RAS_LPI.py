import os
import nibabel as nib
import numpy as np
'''
run time is approx 3-4 min
'''
# set project directory (where all subject directories are)
project_dir = '/Users/antonio/Desktop/atlas_X/'
out_dir = '/Users/antonio/Desktop/atlas_X/atlas'

#make output directory if it does not exist
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
    
# get all subject directories -> first output is directory name
temp_dir = [direct[0] for direct in os.walk(project_dir)]

# only keep dir with the roi subdirectory as there are nested folders in project to subject roi dir
sub_dir = [direct for direct in temp_dir if '/rois' in direct]

# keep track of number of subjects for division
n = len(sub_dir)

# get all tract names by indexing into a subject directory and sorting
# this makes indexing easier as LPI is now odd and RAS is even; also same tracts are stacked together in twos
tract_names = sorted(next(os.walk(sub_dir[0]))[2])

# tract counter
tract_count = 1
# load the files sum and divide to create probability map
for jj in range(len(tract_names)):
    # split tract names for easier searching and saving
    name = tract_names[jj].split('_')      
    
    for ii in range(len(sub_dir)):
        # load the tract for all subs
        img = nib.load(sub_dir[ii]+'/'+tract_names[jj]) 
        
        # initialize the data mats
        if ii == 0:
            data = np.zeros((img.get_fdata()).shape)        
        
        # check if subjects data is binarized
        if np.max(img.get_fdata()) == 1:
            data += img.get_fdata()
            
    # have to match affine transform for output
    input_affine = img.affine
    
    # need to change this
    #n=234 # hard-coded for now to account for non-binarized
    max_sum = np.max(data)
    #normalize
    data = data/max_sum
    
    #remove points < p = 0.5 too much - trying 0.3
    data[data<0.3]=0
    
    # save tract map as nifti
    converted_array = np.array(data,dtype=np.float32)
    new_img = nib.Nifti1Image(converted_array,affine=input_affine) #turn into nifti
    filename = str(tract_count)+'_'+name[3]+'_'+name[0]+'_'+'[min_'+str(np.min(data))+'_'+'max_'+str(np.max(data))+']'+'.nii.gz'
    nib.save(new_img,os.path.join(out_dir+'/',filename)) # save file
    if jj%2:
        tract_count+=1 # update tract counter
import os
import nibabel as nib
import numpy as np
'''
run time is approx 3-4 min
'''
# set project directory (where all subject directories are)
project_dir = '/Users/antonio/Desktop/proj-6396777a6881d56fbfcd0bbc/'
out_dir = '/Users/antonio/Desktop/proj-6396777a6881d56fbfcd0bbc/atlas'

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

# dont save until LPI and RAS for same tract are done
# set counter so that theres no saving until both mats are populated
count = 1
# tract counter
tract_count = 1
# load the files sum and divide to create probability map
for tract in tract_names:
    # split tract names for easier searching and saving
    name = tract.split('_')      
    
    for ii in range(len(sub_dir)):
        # load the tract for all subs
        img = nib.load(sub_dir[ii]+'/'+tract)
        
        # have to match affine transform for output
        input_affine = img.affine 
        
        # initialize the data mats
        if ii == 0 and count == 1:
            data_lpi = np.zeros((img.get_fdata()).shape)
            data_ras = np.zeros((img.get_fdata()).shape)
        
        # sum across subjects
        if 'LPI' in name:
            data_lpi += img.get_fdata()
        if 'RAS' in name:
            data_ras += img.get_fdata()
    
    # once both LPI and RAS exist save
    if count==2: 
        #normalize
        data = data_lpi/n + data_ras/n 
        converted_array = np.array(data,dtype=np.float32)
        new_img = nib.Nifti1Image(converted_array,affine=input_affine) #turn into nifti
        filename = str(tract_count)+'_'+name[0]+'max_prob_'+str(np.max(data))+'.nii.gz'
        nib.save(new_img,os.path.join(out_dir+'/',filename)) # save file
        tract_count+=1 # update tract counter
        count = 0 #reset the counter to 0 
    count+=1 #update count

import xarray as xr

LANDSAT_BANDS = ['lwir11', 'red','blue','green', 'nir08','swir16','swir22']

def mask_clouds(landsat_da):
    mask_bitfields = [1, 2, 3, 4]  # dilated cloud, cirrus, cloud, cloud shadow
    bitmask = 0
    for field in mask_bitfields:
        bitmask |= 1 << field
    
    # select the bands that we're using
    t_bands = ['lwir11']
    r_bands = ['red','blue','green', 'nir08','swir16','swir22']

    bands = r_bands + t_bands 
    
    # select the bands and the qa_pixel 
    landsat_da = landsat_da.sel(band=bands+['qa_pixel'])
    
    # create the mask, 1 where clouds or shadows and 0 elsewhere
    qa = landsat_da.sel(band='qa_pixel').astype('uint16')
    cloudy_bitmask = qa & bitmask  # This is the subset of the qa_pixel pixels that we definitely don't want
    
    # Mask the images with their respective cloud mask, choosing only pixels where "cloud" isn't
    landsat_da = landsat_da.sel(band=bands).where(cloudy_bitmask == 0)
    return landsat_da
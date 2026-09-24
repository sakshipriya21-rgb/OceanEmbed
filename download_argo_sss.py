import copernicusmarine

copernicusmarine.subset(
    dataset_id="cmems_obs-mob_glo_phy-sss_my_multi_P1D",
    variables=["sos"],
    minimum_longitude=72.5,
    maximum_longitude=73.0,
    minimum_latitude=14.0,
    maximum_latitude=14.5,
    start_datetime="2020-08-02T00:00:00",
    end_datetime="2020-08-02T23:59:59",
    output_directory="data/argo_validation",
    output_filename="argo_sss_2020_08_02.nc"
)

print("\nSSS download complete.")

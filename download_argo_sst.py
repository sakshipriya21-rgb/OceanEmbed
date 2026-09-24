import copernicusmarine

copernicusmarine.subset(
    dataset_id="METOFFICE-GLO-SST-L4-REP-OBS-SST",
    variables=["analysed_sst"],
    minimum_longitude=72.5,
    maximum_longitude=73.0,
    minimum_latitude=14.0,
    maximum_latitude=14.5,
    start_datetime="2020-08-02T00:00:00",
    end_datetime="2020-08-02T23:59:59",
    output_directory="data/argo_validation",
    output_filename="argo_sst_2020_08_02.nc"
)

print("\nSST download complete.")
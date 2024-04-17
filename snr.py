import os
import csv
from astropy.io import fits

def extract_fits_header_info(fits_filename):
    header_info = {}

    try:
        with fits.open(fits_filename, ignore_missing_simple=True) as hdul:
            header = hdul[0].header

            # Extract specific information from the header
            header_info['FILENAME'] = os.path.basename(fits_filename)
            header_info['OBSID'] = header.get('OBSID', 'N/A')
            header_info['DATE-OBS'] = header.get('DATE-OBS', 'N/A')
            header_info['DATE-BEG'] = header.get('DATE-BEG', 'N/A')
            header_info['DATE-END'] = header.get('DATE-END', 'N/A')
            header_info['LMJD'] = header.get('LMJD', 'N/A')
            header_info['MJD'] = header.get('MJD', 'N/A')
            header_info['TELESCOP'] = header.get('TELESCOP', 'N/A')
            header_info['RA'] = header.get('RA', 'N/A')
            header_info['DEC'] = header.get('DEC', 'N/A')
            header_info['EXPTIME'] = header.get('EXPTIME', 'N/A')
            header_info['SEEING'] = header.get('SEEING', 'N/A')
            header_info['MOONPHA'] = header.get('MOONPHA', 'N/A')

            # Extract SNR from the extension 'COADD_B'
            try:
                snr = hdul['COADD_B'].header.get('SNR', 'N/A')
                header_info['SNR'] = snr
            except KeyError:
                header_info['SNR'] = 'N/A'

    except OSError as e:
        print(f"Error reading FITS file {fits_filename}: {e}")
        return None

    return header_info

def process_fits_files(output_csv):
    folder_path = os.getcwd()  # Get the current working directory

    # List all FITS files in the folder
    fits_files = [file for file in os.listdir(folder_path) if file.endswith('.fits')]

    # Write header to CSV
    with open(output_csv, 'w', newline='') as csv_file:
        fieldnames = ['FILENAME', 'OBSID', 'DATE-OBS', 'DATE-BEG', 'DATE-END', 'LMJD', 'MJD',
                      'TELESCOP', 'RA', 'DEC', 'EXPTIME', 'SEEING', 'MOONPHA', 'SNR']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Process each FITS file
        for fits_file in fits_files:
            fits_path = os.path.join(folder_path, fits_file)

            try:
                header_info = extract_fits_header_info(fits_path)
                
                # Check if header information was successfully extracted
                if header_info is not None:
                    writer.writerow(header_info)
                else:
                    # Print the name of the file that encountered an error
                    print(f"Error processing FITS file: {fits_file}")

            except Exception as e:
                # Print the name of the file that encountered an error
                print(f"Error processing FITS file: {fits_file}. Error: {e}")

# Example usage
output_csv = 'fits_info_with_snr.csv'  # Output CSV file name

process_fits_files(output_csv)




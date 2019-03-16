#!/bin/bash

# example: bash no_gaps.sh LE070180452014072601T1-SC20180606133026/

PATH_S3="s3://conabio-s3-oregon/linea_base/L7/"
PATH_S3_NO_GAP="s3://conabio-s3-oregon/linea_base/"

function get_scene (){
    echo "Descargando escena" $PATH_S3$1
    mkdir -p $1
    aws s3 cp $PATH_S3$1 $1 --recursive --quiet
}

function fill_nodata (){
    b1=$(find $(pwd) -type f -name "*band1.tif")
    b2=$(find $(pwd) -type f -name "*band2.tif")
    b3=$(find $(pwd) -type f -name "*band3.tif")
    b4=$(find $(pwd) -type f -name "*band4.tif")
    b5=$(find $(pwd) -type f -name "*band5.tif")
    b7=$(find $(pwd) -type f -name "*band7.tif")
    bq=$(find $(pwd) -type f -name "*pixel_qa.tif")
    
    b1_n=${b1##*/}
    b1_f=${b1_n%.tif}

    b2_n=${b2##*/}
    b2_f=${b2_n%.tif}

    b3_n=${b3##*/}
    b3_f=${b3_n%.tif}

    b4_n=${b4##*/}
    b4_f=${b4_n%.tif}

    b5_n=${b5##*/}
    b5_f=${b5_n%.tif}

    b7_n=${b7##*/}
    b7_f=${b7_n%.tif}

    bq_n=${bq##*/}
    bq_f=${bq_n%.tif}

    CALC="0*(A==-9999)+1*(A!=-9999)"
    CALC_QA="0*(A==1)+1*(A!=1)"
    
    echo "Generando máscara para banda 1"
    gdal_calc.py -A $b1 --outfile=$b1_f"_mask.tif" --calc="$CALC" --co="COMPRESS=LZW" --quiet

    echo "Generando máscara para banda 2"
    gdal_calc.py -A $b2 --outfile=$b2_f"_mask.tif" --calc="$CALC" --co="COMPRESS=LZW" --quiet

    echo "Generando máscara para banda 3"
    gdal_calc.py -A $b3 --outfile=$b3_f"_mask.tif" --calc="$CALC" --co="COMPRESS=LZW" --quiet

    echo "Generando máscara para banda 4"
    gdal_calc.py -A $b4 --outfile=$b4_f"_mask.tif" --calc="$CALC" --co="COMPRESS=LZW" --quiet

    echo "Generando máscara para banda 5"
    gdal_calc.py -A $b5 --outfile=$b5_f"_mask.tif" --calc="$CALC" --co="COMPRESS=LZW" --quiet

    echo "Generando máscara para banda 7"
    gdal_calc.py -A $b7 --outfile=$b7_f"_mask.tif" --calc="$CALC" --co="COMPRESS=LZW" --quiet

    echo "Generando máscara para pixel-qa"
    gdal_calc.py -A $bq --outfile=$bq_f"_mask.tif" --calc="$CALC_QA" --co="COMPRESS=LZW" --NoDataValue=0 --quiet

    echo "Fill-nodata para banda 1"
    gdal_fillnodata.py -md 15 -b 1 -nomask -mask $b1_f"_mask.tif" -of GTiff $b1 $b1_f".tif"

    echo "Fill-nodata para banda 2"
    gdal_fillnodata.py -md 15 -b 1 -nomask -mask $b2_f"_mask.tif" -of GTiff $b2 $b2_f".tif"

    echo "Fill-nodata para banda 3"
    gdal_fillnodata.py -md 15 -b 1 -nomask -mask $b3_f"_mask.tif" -of GTiff $b3 $b3_f".tif" 

    echo "Fill-nodata para banda 4"
    gdal_fillnodata.py -md 15 -b 1 -nomask -mask $b4_f"_mask.tif" -of GTiff $b4 $b4_f".tif"

    echo "Fill-nodata para banda 5"
    gdal_fillnodata.py -md 15 -b 1 -nomask -mask $b5_f"_mask.tif" -of GTiff $b5 $b5_f".tif" 

    echo "Fill-nodata para banda 7"
    gdal_fillnodata.py -md 15 -b 1 -nomask -mask $b7_f"_mask.tif" -of GTiff $b7 $b7_f".tif" 

    echo "Fill-nodata para pixel-qa"
    gdal_fillnodata.py -md 15 -b 1 -nomask -mask $bq_f"_mask.tif" -of GTiff $bq $bq_f".tif" 
}

function upload_to_S3 (){
    b1_ng=$(find $(pwd) -maxdepth 1 -type f -name "*band1*")
    b2_ng=$(find $(pwd) -maxdepth 1 -type f -name "*band2*")
    b3_ng=$(find $(pwd) -maxdepth 1 -type f -name "*band3*")
    b4_ng=$(find $(pwd) -maxdepth 1 -type f -name "*band4*")
    b5_ng=$(find $(pwd) -maxdepth 1 -type f -name "*band5*")
    b7_ng=$(find $(pwd) -maxdepth 1 -type f -name "*band7*")
    bq_ng=$(find $(pwd) -maxdepth 1 -type f -name "*pixel_qa*")

    f1_ng=$(find $(pwd) -maxdepth 1 -type f -name "*T1.xml")
    f2_ng=$(find $(pwd) -maxdepth 1 -type f -name "*ANG.txt")
    f3_ng=$(find $(pwd) -maxdepth 1 -type f -name "*MTL.txt")

    b1_nng=${b1_ng##*/}
    b1_ngf=${b1_nng%.tif}

    b2_nng=${b2_ng##*/}
    b2_ngf=${b2_nng%.tif}

    b3_nng=${b3_ng##*/}
    b3_ngf=${b3_nng%.tif}

    b4_nng=${b4_ng##*/}
    b4_ngf=${b4_nng%.tif}

    b5_nng=${b5_ng##*/}
    b5_ngf=${b5_nng%.tif}

    b7_nng=${b7_ng##*/}
    b7_ngf=${b7_nng%.tif}

    bq_nng=${bq_ng##*/}
    bq_ngf=${bq_nng%.tif}

    echo "Subiendo $b1_ng a S3: $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b1_nng"
    aws s3 cp $b1_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b1_nng --quiet

    echo "Subiendo $b2_ng a S3: $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b2_nng"
    aws s3 cp $b2_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b2_nng --quiet

    echo "Subiendo $b3_ng a S3: $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b3_nng"
    aws s3 cp $b3_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b3_nng --quiet

    echo "Subiendo $b4_ng a S3: $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b4_nng"
    aws s3 cp $b4_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b4_nng --quiet

    echo "Subiendo $b5_ng a S3: $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b5_nng"
    aws s3 cp $b5_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b5_nng --quiet

    echo "Subiendo $b7_ng a S3: $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b7_nng"
    aws s3 cp $b7_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$b7_nng --quiet

    echo "Subiendo $bq_ng a S3: $PATH_S3_NO_GAP"L7_NOGAPS/"$1$bq_nng"
    aws s3 cp $bq_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$bq_nng --quiet

    echo "Subiendo $bq_ng a S3: $PATH_S3_NO_GAP"L7_NOGAPS/"$1$bq_nng"
    aws s3 cp $bq_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$bq_nng --quiet

    echo "Subiendo archivos de metadatos"
    aws s3 cp $f1_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$f1_ng --quiet
    aws s3 cp $f2_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$f2_ng --quiet
    aws s3 cp $f3_ng $PATH_S3_NO_GAP"L7_NOGAPS/"$1$f3_ng --quiet


}

function delete_files (){
    echo "Borrando archivos de disco local"
    rm -rf $1
    rm -rf *tif
}

main() {
    get_scene "$@"
    fill_nodata
    upload_to_S3 "$@"
    delete_files "$@"
    printf '\nTerminado!\n'
}

main "$@"

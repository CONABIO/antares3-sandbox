#!/bin/bash

delete=n

function usage()
{
    printf "\n"
    printf "\t\t Fill nodata proccess for Landsat 7 scenes\n"
		printf "\n"
    printf "Usage: bash gaps.sh --path /path/scenes --delete --outdir /output\n"
    printf "Usage: bash gaps.sh --path /path/scenes --outdir /output\n"
    printf "\n"
    printf "  --help  \tPrints this help and exits\n"
    printf "  --path  \tPath to Landsat 7 scenes \n"
    printf "  --delete \tDelete original scenes (default off)\n"
    printf "  --outdir \tOutput directory for filled scenes\n"
    printf "\n"
}

# Works on Linux
getopt --test > /dev/null
if [[ $? -ne 4 ]]; then
    printf "I’m sorry, `getopt --test` failed in this environment.\n"
    exit 1
fi

OPTIONS=hp:do:
LONGOPTIONS=help,path:,delete,outdir

PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")

if [[ $? -ne 0 ]]; then
    # e.g. $? == 1
    #  then getopt has complained about wrong arguments to stdout
    usage
    exit 2
fi

# read getopt’s output this way to handle the quoting right:
eval set -- "$PARSED"

# options are split until we see --
while true; do
    case "$1" in
        --help)
            usage
            exit
            ;;
        --path)
            path="$2"
            shift 2
            ;;
        --delete)
            delete=y
            shift
            ;;
        --outdir)
            outdir="$3"
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            printf "Unknow value argument\n"
            exit 3
            ;;
    esac
done

function check_path_param(){
  # handle non-option arguments
  if [[ -z "$path" ]]; then
      usage
      printf "[ERROR] A path to scene(s) is required.\n"
      exit 4
  fi
  if [ -d "$path" ]; then
    # Take action if $path exists
    check_entry "$@"
  else
    #  Control will jump here if $path does NOT exists
    echo "Error: ${path} not found. Can not continue."
    exit 1
  fi
}

function check_entry(){
  echo "Processing scenes in ${path}"
  for item in ${path}/*
  do
    if [[ -d $item ]]; then
      echo "$item is a directory"
      echo "This script only works with compressed data"
    elif [[ -f $item ]]; then
      #echo "$item is a file"
      if [[ ${item: -3} == ".gz" ]]; then
        get_scene_name "$item"
      fi
    else
      echo "$item is not a valid entry"
      exit 1
    fi
    echo "------------------"
  done
}

function get_scene_name (){
  #echo "untar " $1
  NAME=$(basename $1 .tar.gz)
  fill_nodata_scene $1 $NAME

}

function untar_data(){
  echo "Saving processed data in" $2/$3
  mkdir -p $2/$3
  tar xvzf $1 -C $2/$3
  rm $2/$3/*radsat*
  rm $2/$3/*atmos*
  rm $2/$3/*cloud*
}

function fill_nodata_scene(){
  echo "Procesando fill nodata $1"
  untar_data $1 $outdir $NAME
  for tif in $outdir/$NAME/*.tif
  do
    echo "fill no data para " $tif
  done

}

function delete_original(){
  # Delete the unzipped file after running sen2cor
  echo "deleting original scenes"

}

main() {
    check_path_param "$@"
    #check_entry "$@"
    if [ "$delete" == "y" ]; then
       delete_original "$@"
    fi

}

main "$@"

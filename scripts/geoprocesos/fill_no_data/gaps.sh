#!/bin/bash

show_options() {
    # if no param is given, display a menu and then exit
    (( $# < 1 )) && {
        # display a menu of options
        echo " "
        echo "            MAIN MENU"
        echo
        echo "       -p                Path to scenes"
        echo "       -d                Delete original scenes after fill-nodata completes"
    }
}

function get_scene (){
  echo "Lee escenas de $1"
}

function fill_nodata (){
  echo "Ejecuta fill"
}

function delete_original (){
  echo "Borrando escenas originales"
}

main() {

  if [[ $# -eq 0 ]] ; then
    show_options
    exit 0
  fi

  get_scene "$@"
  fill_nodata
  delete_original "$@"
}

main "$@"

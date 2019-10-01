#!/bin/bash

function get_scene (){
  echo "Lee escena"
}

function fill_nodata (){
  echo "Ejecuta fill"
}

function delete_original (){
  echo "Borrando escenas originales"
}

main() {
    get_scene "$@"
    fill_nodata
    delete_original "$@"
}

main "$@"

package main

import (
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"rbpServer/server"
)

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/", server.Hello)
	router.HandleFunc("/toggle", server.LIFXHandler)
	log.Fatal(http.ListenAndServe(":8080", router))
}

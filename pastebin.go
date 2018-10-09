package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

/*
This code creates a VERY SIMPLE paste bin on a server.
You can crete a random data and assign the token variable below.
The post request must be sent as form url encoded style.
The program stores the posted data on a file
There is no buffer protection in the code.
*/
var secret = "RANDOM_ACCESS_TOKEN"
var file *os.File
var fileName = "pastes"

func main() {
	file, _ = os.OpenFile("fileName", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
	if file == nil {
		panic("Something go wrong, cannot create the file")
	}
	router := mux.NewRouter()
	router.HandleFunc("/paste", Paste).Methods("POST")
	log.Fatal(http.ListenAndServe(":5192", router))
}

// Paste ...
func Paste(w http.ResponseWriter, r *http.Request) {
	err := r.ParseForm()
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Bad request!!!"))
		return
	}
	token := r.Form.Get("token")
	if token == secret {
		data := r.Form.Get("data")
		_, err := file.WriteString(data + "\n")
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("Something go wrong, could not save the data"))
		} else {
			w.WriteHeader(http.StatusOK)
			w.Write([]byte("Content saved succefully"))
		}
	} else {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("Unauthorized Attempt!!!"))
	}
}

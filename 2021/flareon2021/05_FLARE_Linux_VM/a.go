package main

import (
	"os"
	"path/filepath"
	"bytes"
)

func RC4Mod(data []uint8, key []uint8) []uint8 {
	var out []uint8
	var S []uint8
	for i := 0; i < 256; i++ {
		S = append(S, uint8(i))
	}
	// KSA phase
	var k uint8 = 0
	for i := 0; i < 256; i++ {
		k = k + S[i] + key[i % len(key)]
		S[i] , S[k] = S[k] , S[i]
	}
	// PRGA phase
	var i, j uint8 = 0, 0
	var x uint8 = 0
	for _, b := range data {
		i = i + 1
		j = j + S[i]
		S[i] , S[j] = S[j] , S[i]
		rnd := S[S[i] + S[j]]
		out = append(out, b ^ (rnd ^ x))
		x = rnd
	}
	return out
}

func main() {
	key := []uint8("A secret is no longer a secret once someone knows it")
	currentDirectory, _ := os.Getwd()
	encDir := currentDirectory + "/Documents_broken"
	decDir := currentDirectory + "/Documents2"

	filepath.Walk(encDir, func(path string, info os.FileInfo, err error) error {
		if info.IsDir(){
			return nil
		}
		data, _ := os.ReadFile(path)
		data = []uint8(data)
		decData := RC4Mod(data, key)
		decFileName := decDir + "/" + info.Name()[:len(info.Name()) - 7]
		os.WriteFile(decFileName, bytes.Trim([]byte(decData), "\x00"), 0777)
		return nil
	})
}


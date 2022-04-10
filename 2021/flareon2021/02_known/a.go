package main

import (
	"fmt"
	"math/bits"
	"os"
	"encoding/hex"
)

func decryptOnce(data []uint8, key []uint8) []uint8 {
	var result []uint8
	for i := 0; i < 8; i++ {
		decByte := bits.RotateLeft8(key[i] ^ data[i], i) - uint8(i)
		result = append(result, decByte)
	}
	return result
} 

func main() {
	data, _ := os.ReadFile("./Files/critical_data.txt.encrypted")
	data = []uint8(data)
	pngMagic, _ := hex.DecodeString("89504E470D0A1A0A")
	pngMagic = []uint8(pngMagic)
	pngMagicEnc, _ := hex.DecodeString("C7C7251D630DF356")
	pngMagicEnc = []uint8(pngMagicEnc)

	var key []uint8
	for i := 0; i < 8; i++ {
		keyByte := bits.RotateLeft8(pngMagic[i] + uint8(i), -i) ^ pngMagicEnc[i]
		key = append(key, keyByte)
	}
	fmt.Println(key)

	var flag []uint8
	for i := 0; i < len(data); i += 8 {
		flag = append(flag, decryptOnce(data[i:i+8], key)...)
	}
	fmt.Println(string(flag))
}

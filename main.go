package main

import (
	"encoding/xml"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	baseURL := "https://cloudformation-schema.s3.us-west-2.amazonaws.com/"

	resp, err := http.Get(baseURL)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	var root struct {
		XMLName  xml.Name `xml:"ListBucketResult"`
		Contents []struct {
			Key string `xml:"Key"`
		} `xml:"Contents"`
	}

	err = xml.Unmarshal(body, &root)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	var keys []string
	for _, contents := range root.Contents {
		if strings.HasPrefix(contents.Key, "resourcetype/") {
			keys = append(keys, contents.Key)
		}
	}

	for _, key := range keys {
		resp, err := http.Get(baseURL + key)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			continue
		}
		defer resp.Body.Close()

		fileName := filepath.Base(key)
		filePath := filepath.Join(".", fileName)
		body, err := io.ReadAll(resp.Body)
		err = os.WriteFile(filePath, []byte(body), 0644)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			continue
		}
		fmt.Printf("Downloaded %s\n", filePath)
	}
}

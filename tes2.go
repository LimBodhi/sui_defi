package main

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
	"time"

	"golang.org/x/net/html"
)

const (
	MAIN_URL       = "https://academic.ui.ac.id/main/Authentication/"
	LOGIN_URL      = "https://academic.ui.ac.id/main/Authentication/Index"
	CHANGE_ROLE_URL = "https://academic.ui.ac.id/main/Authentication/ChangeRole"
	ISI_IRS_URL    = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"
	SAVE_IRS       = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSave"
	RINGKASAN_URL  = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanSummary"

	USERNAME = ""
	PASSWORD = ""
	TERM     = "Term 1"
)

var SAVEDTEXT string

func main() {
	for {
		tr := &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		}
		client := &http.Client{Transport: tr}

		fmt.Println("Try to login")
		if !login(client) {
			fmt.Println("Login failed. Retrying...")
			continue
		}

		for !changeRole(client) {
			fmt.Println("Failed to change role. Retrying...")
		}

		if !strings.Contains(SAVEDTEXT, TERM) {
			fmt.Printf("War not started %s\n", time.Now().String())
			continue
		}

		var text string
		for {
			fmt.Println("Try to open isi siak page")
			text = getSiakPage(client)
			if text == "" {
				fmt.Println("Failed to open isi siak page. Retrying...")
				continue
			}
			break
		}

		tokenValue := extractToken(text)

		payload := url.Values{
			"tokens":                           {tokenValue},
			"c[CSGE602012_01.00.12.01-2020]":   {"724680-3"},
			"c[CSGE602091_01.00.12.01-2020]":   {"724707-3"},
			"c[CSGE602022_01.00.12.01-2020]":   {"724720-4"},
			"c[CSGE602040_01.00.12.01-2020]":   {"724748-4"},
			"c[CSIM602155_01.00.12.01-2020]":   {"725467-3"},
			"comment":                          {""},
			"submit":                           {"Simpan IRS"},
		}

		fmt.Println("Try to fill IRS")
		for {
			if !fillIRS(client, payload) {
				fmt.Println("Failed to fill IRS. Retrying...")
				continue
			}
			break
		}

		getRingkasan(client)
	}
}

func login(client *http.Client) bool {
	data := url.Values{
		"u": {USERNAME},
		"p": {PASSWORD},
	}
	resp, err := client.PostForm(LOGIN_URL, data)
	if err != nil {
		fmt.Printf("Error during login: %v\n", err)
		return false
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	text := string(body)

	if !strings.Contains(text, "redirecting...") {
		fmt.Println("Terjadi masalah saat melakukan Login ke Siak")
		return false
	}
	if strings.Contains(text, "Login Failed") {
		return false
	}
	return true
}

func changeRole(client *http.Client) bool {
	resp, err := client.Get(CHANGE_ROLE_URL)
	if err != nil {
		fmt.Printf("Error during role change: %v\n", err)
		return false
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	text := string(body)

	if !strings.Contains(text, "WAHYU RIDHO") && !strings.Contains(text, "Mahasiswa") {
		fmt.Println("Gagal dalam mengganti role")
		return false
	}
	SAVEDTEXT = text
	return true
}

func getSiakPage(client *http.Client) string {
	resp, err := client.Get(ISI_IRS_URL)
	if err != nil {
		fmt.Printf("Error getting SIAK page: %v\n", err)
		return ""
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	text := string(body)

	if !strings.Contains(text, "Pengisian IRS") {
		fmt.Println("Gagal dalam membuka halaman Pengisian IRS")
		return ""
	}
	return text
}

func fillIRS(client *http.Client, payload url.Values) bool {
	resp, err := client.PostForm(SAVE_IRS, payload)
	if err != nil {
		fmt.Printf("Error filling IRS: %v\n", err)
		return false
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	text := string(body)

	if strings.Contains(text, "IRS berhasil tersimpan!") {
		fmt.Println("Berhasil tersimpan!")
		return true
	} else {
		fmt.Println("Gagal menyimpan IRS")
		return false
	}
}

func getRingkasan(client *http.Client) bool {
	resp, err := client.Get(RINGKASAN_URL)
	if err != nil {
		fmt.Printf("Error getting ringkasan: %v\n", err)
		return false
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	text := string(body)

	if !strings.Contains(text, "Ringkasan") {
		fmt.Println("Gagal membuka halaman Ringkasan Pengisian IRS")
		return false
	}
	fmt.Println("Berhasil")
	return true
}

func extractToken(htmlContent string) string {
	doc, err := html.Parse(strings.NewReader(htmlContent))
	if err != nil {
		fmt.Printf("Error parsing HTML: %v\n", err)
		return ""
	}

	var tokenValue string
	var f func(*html.Node)
	f = func(n *html.Node) {
		if n.Type == html.ElementNode && n.Data == "input" {
			for _, a := range n.Attr {
				if a.Key == "name" && a.Val == "tokens" {
					for _, v := range n.Attr {
						if v.Key == "value" {
							tokenValue = v.Val
							return
						}
					}
				}
			}
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			f(c)
		}
	}
	f(doc)
	return tokenValue
}
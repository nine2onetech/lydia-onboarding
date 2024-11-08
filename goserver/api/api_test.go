package api

import (
	"fmt"
	"testing"
)

func TestGetBikeStns(t *testing.T) {
	want := 3139
	got, got_stations, _ := GetBikeStns()
	if got != want || len(got_stations) != want {
		t.Errorf("GetBikeStns() got = %v, want %v", got, want)
	}
}

func TestGetBikeStnStatus(t *testing.T) {
	want := 2700
	got, _ := GetBikeStnStatus()
	fmt.Print(len(got))
	if len(got) != want {
		t.Errorf("GetBikeStnStatus() got = %v, want %v", len(got), want)
	}
}

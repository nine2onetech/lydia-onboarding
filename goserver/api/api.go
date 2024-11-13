package api

import (
	"encoding/json"
	"fmt"
	"io"
	"math"
	"net/http"
	"strconv"
)

var key = "736c567a516c696e3131355475534258"
var limit = 1000

// 구조체 타입을 담아야하므로 빈 interface 사용
func parseApiResponse(resp *http.Response, respType interface{}) error {
	// 함수 종료 시, 네트워크 연결 끊음
	defer resp.Body.Close()

	body, readErr := io.ReadAll(resp.Body)
	if readErr != nil {
		return fmt.Errorf("error reading api response : %w", readErr)
	}
	json.Unmarshal(body, respType)
	return nil
}

func GetBikeStns() (int, []Station, error) {
	baseURL := "http://openapi.seoul.go.kr:8088/%s/json/tbCycleStationInfo"
	url := fmt.Sprintf(baseURL, key) + fmt.Sprintf("/1/%d", limit)
	resp, err := http.Get(url)
	if err != nil {
		return 0, []Station{}, fmt.Errorf("cannot get station list: %w", err)
	}
	var apiResponse GetBikeStnApiResponse
	parseErr := parseApiResponse(resp, &apiResponse)
	if parseErr != nil {
		return 0, []Station{}, parseErr
	}

	totalStations := apiResponse.StationInfo.Row
	count, _ := strconv.Atoi(apiResponse.StationInfo.ListTotalCount)

	if count > limit {
		cursor := limit + 1
		loopsToRun := math.Ceil(float64(count-limit) / float64(limit))
		for i := 0; i < int(loopsToRun); i++ {
			url := fmt.Sprintf(baseURL, key) + fmt.Sprintf("/%d/%d", cursor, cursor+limit-1)
			resp, err := http.Get(url)
			if err != nil {
				return 0, []Station{}, fmt.Errorf("cannot get station list: %w", err)
			}
			cursor += limit
			var apiResponse GetBikeStnApiResponse
			parseErr := parseApiResponse(resp, &apiResponse)
			if parseErr != nil {
				return 0, []Station{}, parseErr
			}
			totalStations = append(totalStations, apiResponse.StationInfo.Row...)
		}
	}

	return count, totalStations, nil
}

func GetBikeStnStatus() ([]StationStatus, error) {
	baseURL := "http://openapi.seoul.go.kr:8088/%s/json/bikeList"
	url := fmt.Sprintf(baseURL, key) + fmt.Sprintf("/1/%d", limit)
	resp, err := http.Get(url)
	if err != nil {
		return []StationStatus{}, fmt.Errorf("cannot get station status: %w", err)
	}
	var apiResponse GetStnStatusApiResponse
	parseErr := parseApiResponse(resp, &apiResponse)
	if parseErr != nil {
		return []StationStatus{}, parseErr
	}

	statuses := apiResponse.RentBikeStatus.Row

	// 해당 API 의 경우, list_total_count 에 전체 entry 개수를 포함하지 않으므로
	// list_total_count 가 limit 인 1000 보다 작아질 때까지 반복하여 전체 리스트를 취득함
	if apiResponse.RentBikeStatus.ListTotalCount == limit {
		cursor := limit + 1
		for {
			url := fmt.Sprintf(baseURL, key) + fmt.Sprintf("/%d/%d", cursor, cursor+limit-1)
			resp, err := http.Get(url)
			if err != nil {
				return []StationStatus{}, fmt.Errorf("cannot get station status: %w", err)
			}
			var apiResponse GetStnStatusApiResponse
			parseErr := parseApiResponse(resp, &apiResponse)
			if parseErr != nil {
				return []StationStatus{}, parseErr
			}
			statuses = append(statuses, apiResponse.RentBikeStatus.Row...)
			if apiResponse.RentBikeStatus.ListTotalCount < limit {
				break
			}
			cursor += limit
		}
	}

	return statuses, nil
}

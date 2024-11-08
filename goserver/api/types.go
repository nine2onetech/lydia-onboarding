package api

// station list

type Station struct {
	STALOC   string `json:"STA_LOC"`
	RENTID   string `json:"RENT_ID"`
	RENTNO   string `json:"RENT_NO"`
	RENTNM   string `json:"RENT_NM"`
	RENTIDNM string `json:"RENT_ID_NM"`
	HOLDNUM  string `json:"HOLD_NUM"`
	STAADD1  string `json:"STA_ADD1"`
	STAADD2  string `json:"STA_ADD2"`
	STALAT   string `json:"STA_LAT"`
	STALNG   string `json:"STA_LONG"`
}

type Result struct {
	CODE    string `json:"CODE"`
	MESSAGE string `json:"MESSAGE"`
}

type StationInfo struct {
	ListTotalCount string    `json:"list_total_count"`
	Result         Result    `json:"RESULT"`
	Row            []Station `json:"row"`
}

type GetBikeStnApiResponse struct {
	StationInfo StationInfo `json:"stationInfo"`
}

// station status

type StationStatus struct {
	StationName string `json:"stationName"`
	BikeCnt     string `json:"parkingBikeTotCnt"`
	StationId   string `json:"stationId"`
}

type RentBikeStatus struct {
	ListTotalCount int             `json:"list_total_count"`
	Row            []StationStatus `json:"row"`
}

type GetStnStatusApiResponse struct {
	RentBikeStatus RentBikeStatus `json:"rentBikeStatus"`
}

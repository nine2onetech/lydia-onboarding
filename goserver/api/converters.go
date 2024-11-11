package api

// API response type -> Protobuf message type
import (
	bpb "goserver/protogen/bike"
	"strconv"
)

// Station -> Station(pb)
func StationToStationPb(s Station) *bpb.Station {
	lat, _ := strconv.ParseFloat(s.STALAT, 32)
	lng, _ := strconv.ParseFloat(s.STALNG, 32)
	hold_num, _ := strconv.Atoi(s.HOLDNUM)

	return &bpb.Station{
		StnGrpName: s.STALOC,
		StnId:      s.RENTID,
		StnNum:     s.RENTNO,
		StnName:    s.RENTNM,
		StnAddr_1:  s.STAADD1,
		StnAddr_2:  s.STAADD2,
		StnLat:     float32(lat),
		StnLng:     float32(lng),
		HoldNum:    int32(hold_num),
	}
}

func StationsToStationPbList(stations []Station) []*bpb.Station {
	pbs := make([]*bpb.Station, len(stations))
	for i, stn := range stations {
		pbs[i] = StationToStationPb(stn)
	}
	return pbs
}

// StationStatus -> StationStatus(pb)

func StationStatusToStationStatusPb(ss StationStatus) *bpb.StationStatus {
	parked_bike_count, _ := strconv.Atoi(ss.BikeCnt)
	return &bpb.StationStatus{
		StnId: ss.StationID, StnName: ss.StationName, ParkedBikeCnt: int32(parked_bike_count),
	}
}

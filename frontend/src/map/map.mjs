import $ from 'jquery'
import L from 'leaflet'
import 'leaflet.markercluster'
import 'leaflet.featuregroup.subgroup'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import '../css/map.css'

export class MapViewPage {

    constructor(options) {
        this.options = {
            mapViewContainerId: '',
            aURL : '',
            bURL : '',
            aListURL  : '',
            bListURL   : '',
            tileURL: '',
            tileServer: '',
            mapAttribution: '',
            // eslint-disable-next-line no-unused-vars
            createPopupTextA :  (countrycode,city, plz, count, url) => '',

            // eslint-disable-next-line no-unused-vars
            createPopupTextB :  (countrycode,city, plz, count, url) => '',

            // eslint-disable-next-line no-unused-vars
            createACountText: (count) => '',

            // eslint-disable-next-line no-unused-vars
            createBCountText: (count) => '',

            ...options // merge with supplied options
        }

        this.mapObject = null
    }

    createFacilityIcon(count) {
        return L.divIcon({
            className: 'leaflet-marker-icon marker-cluster marker-cluster-single leaflet-zoom-animated leaflet-interactive facilityMarker',
            html: `<div><span>${count}</span></div>`,
            iconSize: [40, 40],
            popupAnchor: [-10,-10],
        })
    }

    createSupporterIcon(count) {
        return L.divIcon({
            className: 'leaflet-marker-icon marker-cluster marker-cluster-single leaflet-zoom-animated leaflet-interactive supporterMarker',
            html: `<div><span>${count}</span></div>`,
            iconSize: [40, 40],
        })
    }

    cssClassedIconCreateFunction(cssClass) {
        return (function (cluster) {
            let childCount = cluster.getChildCount()
            let cssClasses = ['marker-cluster']
            let c = ' marker-cluster-'
            if (childCount < 10) {
                c += 'small'
            } else if (childCount < 100) {
                c += 'medium'
            } else {
                c += 'large'
            }
            cssClasses.push(c)
            cssClasses.push(cssClass)
            return new L.DivIcon({
                html: '<div><span>' + childCount + '</span></div>',
                className: cssClasses.join(' '),
                iconSize: new L.Point(40, 40)
            })
        })
    }

    initializeMap() {
        let mapOptions = {
            center: [51.13, 10.018],
            zoom: 6
        }

        const defaultTileLayerOptions = {
            attribution: this.options.mapAttribution,
            maxZoom: 18,
            preferCanvas: true,
        }

        const mapBoxSpecificTileLayerOptions = {
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
        }

        let tileLayerOptions = defaultTileLayerOptions
        if (this.options.tileServer === 'mapbox') {
            tileLayerOptions = {
                ...tileLayerOptions,
                ...mapBoxSpecificTileLayerOptions,
            }
        }

        this.mapObject = L.map(this.options.mapViewContainerId,mapOptions)
        L.tileLayer(this.options.tileURL, tileLayerOptions).addTo(this.mapObject)

        // Enhance MarkerCluster - override getChildCount
        L.MarkerCluster.prototype.getChildCount = function (){
            const children = this.getAllChildMarkers()
            return children.reduce((sum,marker) => (sum + marker.options.itemCount),0)
        }

    }

    onResizeWindow() {
        let height = $(window).height()
        let navHeight = $('.navbar').outerHeight()
        let searchHeight = $('.search-map').innerHeight()
        let footerHeight = $('.footer').innerHeight()
        let isSearchBarActive = document.getElementById('hospital_navbar') !== null
        let newHeight = height - navHeight - ( isSearchBarActive ? searchHeight : 0 ) - footerHeight
        $(document.getElementById(this.options.mapViewContainerId)).height(newHeight)
        this.mapObject.invalidateSize()
    }

    registerEventHandlers(window) {
        $(window).on('resize', () => { this.onResizeWindow() }).trigger('resize')
    }

    async loadMapMarkers() {
        let [ aParticipants, bParticipants ] = await Promise.all([$.get(this.options.aURL),$.get(this.options.bURL)])

        let bParticipantsClusterMarkerGroup = L.markerClusterGroup({
            iconCreateFunction: this.cssClassedIconCreateFunction('facilityMarker'),
        })
        let bParticipantsMarkers = L.featureGroup.subGroup(bParticipantsClusterMarkerGroup, this.createMapMarkers(bParticipants,(lat,lon,countrycode,city,plz,count) => {
            return L.marker([lon,lat],{
                icon:  this.createFacilityIcon(count),
                itemCount: count,
            }).bindPopup(this.options.createPopupTextB(countrycode,city, plz, count, this.options.bListURL.replace('COUNTRYCODE',countrycode).replace('PLZ',plz)))
        }))

        let aParticipantsClusterMarkerGroup = L.markerClusterGroup({
            iconCreateFunction: this.cssClassedIconCreateFunction('supporterMarker'),
        })
        let aParticipantsMarkers = L.featureGroup.subGroup(aParticipantsClusterMarkerGroup, this.createMapMarkers(aParticipants,(lat,lon,countrycode,city,plz,count) => {
            return L.marker([lon,lat],{
                icon:  this.createSupporterIcon(count),
                itemCount: count,
            }).bindPopup(this.options.createPopupTextA(countrycode,city, plz, count, this.options.aListURL.replace('COUNTRYCODE',countrycode).replace('PLZ',plz)))
        }))

        aParticipantsClusterMarkerGroup.addTo(this.mapObject)
        aParticipantsMarkers.addTo(this.mapObject)
        bParticipantsClusterMarkerGroup.addTo(this.mapObject)
        bParticipantsMarkers.addTo(this.mapObject)

        const countItems = (o) => {
            let count = 0
            for (let countryCode in o) {
                for (let zipCode in o[countryCode]) {
                    count += o[countryCode][zipCode].count
                }
            }
            return count
        }

        let overlays = {}
        overlays[this.options.createBCountText(countItems(bParticipants))] = bParticipantsMarkers
        overlays[this.options.createACountText(countItems(aParticipants))] = aParticipantsMarkers

        bParticipantsMarkers.addTo(this.mapObject)

        L.control.layers(null, overlays, { collapsed: false, position: 'topright' }).addTo(this.mapObject)
    }

    createMapMarkers(markers, createMarkerFunction) {
        let markerArray = []

        for (let countryCode in markers) {
            for (let zipCodeKey in markers[countryCode]) {
                let zipCode = markers[countryCode][zipCodeKey]
                markerArray.push(createMarkerFunction(zipCode.latitude, zipCode.longitude, countryCode, zipCode.city, zipCode.plz, zipCode.count))
            }
        }

        return markerArray
    }

}

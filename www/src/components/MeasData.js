import React, { useEffect, useRef, useState } from "react"

export default function MeasData(props){
    const {data} = props
    
   
    // 'centroid_x_px' : "Centroid X [px]",
    // 'centroid_y_px' : self.centroid_y_px if self.centroid_y_px is not None else 0,
    // 'centroid_center_dist_x_px' : self.centroid_center_dist_x_px,
    // 'centroid_center_dist_y_px' : self.centroid_center_dist_y_px,
    // 'centroid_center_dist_x_um'  : round(self.pixToUm(self.centroid_center_dist_x_px)-self.center_x_um, 2),
    // 'centroid_center_dist_y_um'  : round(self.pixToUm(self.centroid_center_dist_y_px)-self.center_y_um, 2),
    // 'beam_width_px' : self.beam_width_px,
    // 'beam_height_px' : self.beam_height_px,
    // 'beam_width_um' : self.pixToUm(self.beam_width_px),
    // 'beam_height_um' : self.pixToUm(self.beam_height_px),
    // 'beam_volume_px' : self.beam_volume_px,
    
    return <div>
        <h2>Measurement data</h2>
        <table className="ui very compact celled table">
            <thead>
                <tr>
                    <th className="eight wide">Param</th>
                    <th className="eight wide">Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Centroid X [um]</td>
                    <td>{data.centroid_center_dist_x_um}</td>
                </tr>
                <tr>
                    <td>Centroid Y [um]</td>
                    <td>{data.centroid_center_dist_y_um}</td>
                </tr>
                <tr>
                    <td>Centroid width [um]</td>
                    <td>{data.beam_width_um}</td>
                </tr>
                <tr>
                    <td>Centroid height [um]</td>
                    <td>{data.beam_height_um}</td>
                </tr>
            </tbody>
        </table>
    </div>
}
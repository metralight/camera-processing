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
    
    return <div style={{marginTop: "30px"}}>
        <h2>Position X</h2>
        <h1 style={{fontSize:"55px", marginTop: "0.3em"}}>{data.centroid_center_dist_x_um}&nbsp;&micro;m</h1>
        
        <h2>Position Y</h2>
        <h1 style={{fontSize:"55px", marginTop: "0.3em"}}>{data.centroid_center_dist_y_um}&nbsp;&micro;m</h1>

    
        <h2>Width X</h2>
        <h1 style={{fontSize:"55px", marginTop: "0.3em"}}>{data.beam_width_um}&nbsp;&micro;m</h1>

    
        <h2>Width Y</h2>
        <h1 style={{fontSize:"55px", marginTop: "0.3em"}}>{data.beam_height_um}&nbsp;&micro;m</h1>

        
    </div>
}
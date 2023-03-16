import React from "react";

export default function Loader  (props){
    const {text, size, children} = props;
    return <div className="ui active inverted dimmer">
        <p></p>
            <div className={"ui active centered inline text loader " + (size ? size : "massive")}>
                {text ? text : "Loading data"} 
            </div>
        <p></p>
        <p></p>
            {
                children ? <div className="">
                    {children}
                </div> : null
            }
        <p></p>
    </div>
}
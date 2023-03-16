import React, { Component } from 'react';
import PropTypes from 'prop-types';

export default class Modal extends Component {

	constructor(props) {
		super(props);

		this.modalRef = React.createRef();
	}
	
	componentDidMount(){
		window.$(this.modalRef.current).modal({
			// dimmerSettings: { opacity: 0 },
			detachable : false, //bez teto optiony vyjme semantic modal z domu a nefunguje react events
			centered : this.props.centered,
			observeChanges : true,
            onHide : () => {
                if (this.props.beforeClose){
                    this.props.beforeClose()
                }
            }
		});
	}


	showModal(){
		window.$(this.modalRef.current).modal("show");
	}

	closeModal(){
        if (this.props.beforeClose){
            this.props.beforeClose()
        }
		window.$(this.modalRef.current).modal("hide");
	}

	render() {
		return (
			<div className={"ui " + this.props.size + " " + this.props.addClass + " modal"} ref={this.modalRef} >
				<i className="close icon"></i>
				<div className="content">
					{this.props.children}
				</div>
				{ this.props.actions ? 
					<div className="actions">
						{this.props.actions}
					</div>
					:
					""
				}
			</div>
		);
	}
}

Modal.propTypes = {
	addClass : PropTypes.string,
	size : PropTypes.string,
	centered : PropTypes.bool
}

Modal.defaultProps = {
	size : "large",
	centered : true
}



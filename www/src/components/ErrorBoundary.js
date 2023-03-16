import React from "react";

export default class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { componentError: null, componentErrorInfo: null };
    }

    componentDidCatch(error, errorInfo) {
        // Catch errors in any components below and re-render with error message
        this.setState({
            componentError: error,
            componentErrorInfo: errorInfo
        })
        // You can also log error messages to an error reporting service here
    }

    render() {
        if (this.state.errorInfo) {
            // Error path
            return (
                <div className="ui error message">
                    <h2>Application error occured</h2>
                    <details style={{ whiteSpace: 'pre-wrap' }}>
                        {this.state.componentError && this.state.componentError.toString()}
                        <br />
                        {this.state.componentErrorInfo.componentStack}
                    </details>
                </div>
            );
        }
        // Normally, just render children
        return this.props.children;
    }
}
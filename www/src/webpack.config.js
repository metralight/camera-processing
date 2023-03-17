const path = require("path");
const webpack = require("webpack");

module.exports = {
	entry: "./index.js",
	mode: "development",
	module: {
		rules: [
			{
				test: /\.(js|jsx)$/,
				exclude: /(node_modules|bower_components)/,
				loader: "babel-loader",
				options: {
					presets: ["@babel/env", "@babel/preset-react"],
					plugins: ["@babel/plugin-transform-runtime"]
				}
			},
			{
				test: /\.css$/,
				use: ["style-loader", "css-loader"]
			}
		]
	},
	devtool : "source-map",
	resolve: { extensions: ["*", ".js", ".jsx"] },
	output: {
		path: path.resolve(__dirname, "../public"), //kam generovat vystup kompilace
		publicPath: "./", //slozka kam generovat public assets
		filename: "cameraProcessing.js"
	},
	performance : {
		maxEntrypointSize: 512000,
    	maxAssetSize: 512000
	}
	// devServer: {
	// 	contentBase: path.join(__dirname, "../"), //odkud servirovat vystup dev serveru
	// 	port: 3000,
	// 	publicPath: "http://localhost:3000/", //zde videt vystup dev serveru, ale ten neumi komunikovat s backendem na portu 1945 (TODO)
	// 	hotOnly: true
	// },
	// plugins: [new webpack.HotModuleReplacementPlugin()]
};
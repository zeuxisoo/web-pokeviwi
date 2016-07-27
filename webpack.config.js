var webpack = require("webpack");
var vue = require("vue-loader");
var ExtractTextPlugin = require("extract-text-webpack-plugin");

var cssLoader = ExtractTextPlugin.extract("style-loader", "css-loader?sourceMap!postcss-loader");

var publicPath = "/static/build/";

module.exports = {
    entry: ["./resources/assets/app.js"],

    output: {
        path: __dirname + publicPath,
        filename: 'bundle.js',
        publicPath: publicPath,
        pathinfo: true
    },

    module: {
        loaders: [{
            test: /\.vue$/,
            loader: 'vue-loader'
        }, {
            test: /\.js$/,
            loader: "babel-loader",
            exclude: /node_modules/,
            query: {
                presets: ['es2015', 'stage-0'],
                plugins: ['transform-runtime']
            }
        }, {
            test: /\.css$/,
            loader: cssLoader
        }, {
            test: /\.woff(2)?(\?v=\d+\.\d+\.\d+)?$/,
            loader: "url-loader?limit=10000&minetype=application/font-woff"
        }, {
            test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
            loader: "url-loader?limit=10000&mimetype=application/octet-stream"
        }, {
            test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
            loader: "file-loader"
        }, {
            test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
            loader: "url-loader?limit=10000&mimetype=image/svg+xml"
        }, {
            test: /\.json$/,
            loader: "json-loader",
        }]
    },

    vue: {
        css: cssLoader
    },

    babel: {
        presets: ['es2015', 'stage-0'],
        plugins: ['transform-runtime']
    },

    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery"
        })
    ],
}

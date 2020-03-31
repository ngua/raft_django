const path = require("path")
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: './react/main.jsx',

  output: {
    path: path.resolve('./bundles/'),
    filename: '[name]-[hash].js',
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
         use: [
           {
             loader: 'babel-loader'
           }
        ]
      }
    ],
  },

  resolve: {
    extensions: ['*', '.js', '.jsx']
  }
}

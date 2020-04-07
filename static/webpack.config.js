const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: {
    chat: './react/chat.jsx',
    admin: './react/admin.jsx'
  },

  output: {
    path: path.resolve('./bundles/'),
    filename: '[name].js',
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
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader'
        ]
      }
    ]
  },

  resolve: {
    extensions: ['*', '.js', '.jsx']
  }
}

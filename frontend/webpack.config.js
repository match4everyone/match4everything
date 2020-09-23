const fs = require('fs')
const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const CompressionPlugin = require('compression-webpack-plugin')
const FaviconsWebpackPlugin = require('favicons-webpack-plugin')
const VueLoaderPlugin = require('vue-loader/lib/plugin')

module.exports = (env, argv) => {
    // Generate entry points from all .js files in src root
    const srcDir = path.resolve(__dirname, 'src')
    const entryPoints = fs
        .readdirSync(srcDir)
        .filter((fileName) => /\.js$/.test(fileName))
        .reduce((returnObject,fileName) => {
            let bundleName = fileName.split('.').slice(0,-1)
            returnObject[bundleName] = path.resolve(srcDir, fileName)
            return returnObject
        },{})

    let configuration = {
        watchOptions: {
            ignored: /node_modules/,
        },
        externals: {
            django: 'django',
        },
        context: __dirname,
        performance: {
            maxEntrypointSize: 600000,
            maxAssetSize: 400000
        },
        resolve: {
            alias: {
                'vue$': 'vue/dist/vue.esm.js'
            },
            extensions: ['.wasm', '.mjs', '.js', '.json','.vue'],
        },
        module: {
            rules: [
                {
                    test: /\.vue$/,
                    loader: 'vue-loader'
                },
                {
                    test: /\.css$/,
                    use: [
                        'vue-style-loader',
                        'style-loader',
                        'css-loader'
                    ]
                },
                {
                    test: /\.(png|jpg|gif)$/i,
                    use: [
                        {
                            loader: 'url-loader',
                            options: {
                                limit: 8192,
                                esModule: false,
                            },
                        },
                    ],
                },
                {
                    test: /\.m?js$/,
                    enforce: 'pre',
                    loader: 'eslint-loader',
                    exclude: /node_modules/,
                    options: {
                        emitWarning: true,
                        configFile: './.eslintrc.js',
                    }
                },
                {
                    test: /\.m?js$/,
                    exclude: /(node_modules|bower_components)/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            plugins: [],
                            presets: [
                                ['@babel/preset-env', {
                                    debug: false,
                                    useBuiltIns: 'usage',
                                    corejs: 3,
                                    targets: {
                                        'browsers': [
                                            '> 0.25%, not dead',
                                            'ios >= 11'
                                        ]
                                    }
                                }]
                            ]
                        }
                    }
                },
                {
                    test: /\.(scss)$/,
                    use: [{
                        loader: 'style-loader', // inject CSS to page
                    }, {
                        loader: 'css-loader', // translates CSS into CommonJS modules
                        options: {
                            sourceMap: true,
                        },
                    }, {
                        loader: 'postcss-loader', // Run post css actions
                        options: {
                            plugins: function () { // post css plugins, can be exported to postcss.config.js
                                return [
                                    require('precss'),
                                    require('autoprefixer')
                                ]
                            }
                        }
                    }, {
                        loader: 'sass-loader', // compiles Sass to CSS
                        options: {
                            sourceMap: true,
                        },
                    }]
                },
                {
                    test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                    use: [
                        {
                            loader: 'url-loader',
                            options: {
                                limit: 8192,
                            },
                        }
                    ]
                }
            ]
        },
        entry: {
            vendor: ['bootstrap','jquery','leaflet','leaflet.markercluster','leaflet.featuregroup.subgroup'],
            ...entryPoints,  // generated from src/*.js
        },
        output: {
            filename: '[name]-[hash].js',
            chunkFilename: '[name]-[hash].js',
            path: path.resolve(__dirname, 'dist'),
            publicPath: '/static/'
        },
        optimization: {
            splitChunks: {
                cacheGroups: {
                    vendor: {
                        chunks: 'initial',
                        name: 'vendor',
                        test: 'vendor',
                        enforce: true
                    },
                }
            },
        },
        plugins: [
            new CleanWebpackPlugin({
                verbose: true,
                cleanOnceBeforeBuildPatterns: [
                    '**/*',                 // Remove all files
                    '!favicon'              // Except for favicon stuff, that is expensive to build and only built on production run
                ],
            }),
            new BundleTracker({
                path: path.resolve(__dirname, 'dist'),
                filename: 'webpack-stats.json',
                logTime: true,
                indent: '\t',
            }),
            new FaviconsWebpackPlugin({
                logo: path.resolve(__dirname, 'src', 'logo', 'logo.svg'),
                cache: true,
                // path relative to webpack dir, find it in frontend/dist folder
                outputPath: 'favicon',
                // Prefix path for generated assets in generated html
                prefix: 'favicon',
                inject: false,
                devMode: 'webapp',
                mode: 'webapp',
                favicons: {
                    appName: 'match4everyone',
                    appShortName: 'm4e',
                    appDescription: 'We match everyone',
                    background: '#fff',
                    theme_color: '#fff', // In theory, importing vars from scss should be easy, but I can't get it to work.
                    // Idea in: https://medium.com/tarkalabs-til/use-sass-variables-in-javascript-8ce60b5e5e56
                    url: 'http://m4h.com/',
                    display: 'browser',
                    scope: '/',
                    start_url: '/',
                    version: 1.0,
                    // Note that this is relative to outputPath from Plugin above
                    html: 'favicons.html',
                    pipeHTML: true,
                    replace: true
                }
            }),
            new VueLoaderPlugin(),
        ],
    }

    if (argv.mode === 'development') {
        console.log('Running in development mode')
        configuration.mode = 'development'
        configuration.devtool = 'eval-source-map'
    } else {
        console.log('Running in production mode')
        const TerserPlugin = require('terser-webpack-plugin')
        configuration.mode = 'production'
        configuration.optimization = {
            ...configuration.optimization,
            minimize: true,
            minimizer: [new TerserPlugin()],
        }
        configuration.plugins.push(new CompressionPlugin())
    }

    return configuration

}

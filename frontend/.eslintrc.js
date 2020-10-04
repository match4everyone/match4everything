module.exports = {
    root: true,
    'env': {
        'browser': true,
        'es6': true,
        'node': true,

    },
    'extends': [
        'plugin:vue/essential',
        'eslint:recommended',
    ],
    'globals': {
        'Atomics': 'readonly',
        'SharedArrayBuffer': 'readonly'
    },
    'parser': 'vue-eslint-parser',
    'parserOptions': {
        'parser': 'babel-eslint',
        'sourceType': 'module'
    },
    'plugins': ['vue'],
    'rules': {
        'indent': [
            'error',
            4
        ],
        'linebreak-style': [
            'error',
            'unix'
        ],
        'quotes': [
            'error',
            'single'
        ],
        'semi': [
            'error',
            'never'
        ]
    },
    'overrides': [
        {
          'files': [ '**/*.vue' ],
          'rules': {
            'indent': [ 'error', 2 ]
          }
        }
      ]

}

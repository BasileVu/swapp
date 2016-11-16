module.exports = function(grunt) {
    grunt.initConfig({
        copy: {
            main: {
                files: [
                    {
                        expand: true,
                        src: ['node_modules/font-awesome/fonts/*'],
                        dest: 'static/public/fonts/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/tether/dist/js/tether.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/imagesloaded/imagesloaded.pkgd.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/jquery/dist/jquery.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/bootstrap/dist/js/bootstrap.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/packery/dist/isotope.pkgd.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/flickity/dist/flickity.pkgd.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/jquery-match-height/dist/jquery.matchHeight.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/zone.js/dist/zone.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/reflect-metadata/Reflect.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/systemjs/dist/system.src.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }
                ]
            }
        },
        sass: {
            dist: {
                files: {
                    'static/public/css/styles.css': 'static/scss/styles.scss'
                }
            }
        },
        watch: {
            styles: {
                expand: true,
                files: ['**/*.scss'],
                tasks: ['sass']
            },
            livereload: {
                files : [
                    '**/static/public/js/*.js',
                    '**/templates/**/*.html',
                    '**/static/public/css/*.css',
                    '**/static/scss/*.scss',
                    '**/*.py'
                ],
                options: {
                    livereload: 8080
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Default task(s).
    grunt.registerTask('default', ['copy', 'sass']);
};
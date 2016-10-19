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
                        src: ['node_modules/jquery/dist/jquery.js'],
                        dest: 'static/public/js/',
                        flatten: true
                    }, {
                        expand: true,
                        src: ['node_modules/bootstrap/dist/js/bootstrap.js'],
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
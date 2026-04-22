allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

val newBuildDir: Directory =
    rootProject.layout.buildDirectory
        .dir("../../build")
        .get()
rootProject.layout.buildDirectory.value(newBuildDir)

subprojects {
    val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
    project.layout.buildDirectory.value(newSubprojectBuildDir)
}
subprojects {
    project.evaluationDependsOn(":app")
}

subprojects {
    val fixProject = Action<Project> {
        // Force modern build tools to resolve the 25.0.2 error
        try {
            extensions.findByType(com.android.build.gradle.BaseExtension::class.java)?.apply {
                buildToolsVersion = "36.0.0"
                if (namespace == null) {
                    namespace = "com.cutisia.app.plugins.${name.replace("-", "_")}"
                }
            }
        } catch (e: Exception) { }

        // Global fix for 'lStar' resource linking error by bypassing validation for legacy plugins
        tasks.withType(com.android.build.gradle.tasks.VerifyLibraryResourcesTask::class.java).configureEach {
            enabled = false
        }

        // Force a version that satisfy image_picker but without causing unnecessary conflicts
        configurations.all {
            resolutionStrategy.eachDependency {
                if (requested.group == "androidx.core" && (requested.name == "core" || requested.name == "core-ktx")) {
                    useVersion("1.13.1")
                }
            }
        }
    }
    if (state.executed) {
        fixProject.execute(this)
    } else {
        afterEvaluate { fixProject.execute(this) }
    }
}

tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}

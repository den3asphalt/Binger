/*
 * Copyright 2015 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.gradle.performance.fixture;

import org.gradle.performance.measure.MeasuredOperation;

public class BuildExperimentListenerAdapter implements BuildExperimentListener {
    @Override
    public GradleInvocationCustomizer createInvocationCustomizer(BuildExperimentInvocationInfo invocationInfo) {
        return noOpCustomizer;
    }

    @Override
    public void beforeInvocation(BuildExperimentInvocationInfo invocationInfo) {

    }

    @Override
    public void afterInvocation(BuildExperimentInvocationInfo invocationInfo, MeasuredOperation operation, MeasurementCallback measurementCallback) {

    }

    private static GradleInvocationCustomizer noOpCustomizer = new GradleInvocationCustomizer() {
        @Override
        public GradleInvocationSpec customize(GradleInvocationSpec invocationSpec) {
            return invocationSpec;
        }
    };
}
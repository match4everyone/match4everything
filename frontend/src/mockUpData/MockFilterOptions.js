export { mockOptions }

const mockOptions = [
    {
        type: 'PropertyGroup',
        name: 'info_supp',
        label:'Information about your support',
        help_text:'We need to know this because it is important for someone.',
        properties: [
            {
                name: 'pref_area',
                label: 'Preferred Area of Help',
                type: 'MultipleChoiceProperty',
                help_text: 'We need to know this because it is important for someone.',
                choices: [
                    {
                        value: 'ME',
                        caption: 'Medical Practice'
                    },
                    {
                        value: 'PD',
                        caption: 'Public Health Department and other Institutions'
                    },
                    {
                        value: 'HO',
                        caption: 'Hospital'
                    },
                    {
                        value: 'ES',
                        caption: 'Emergency Services'
                    },
                    {
                        value: 'PH',
                        caption: 'Pharmacy'
                    },
                    {
                        value: 'NF',
                        caption: 'Nursing Facilities'
                    },
                    {
                        value: 'LA',
                        caption: 'Laboratory'
                    },
                    {
                        value: 'MP',
                        caption: 'Medical Practice'
                    },
                ]
            }
        ]
    }
]

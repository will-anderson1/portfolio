'use client';

import { Card, CardContent, Typography, Dialog, DialogTitle, DialogContent, DialogActions, Button, Box } from '@mui/material';
import React, { useState } from 'react';
import EducationCard from './components/EducationCard';
import WorkCard from './components/WorkCard';
import InfoModal from './components/InfoModal';

// Data structures for education and work experiences
const educationData = [
  {
    degree: 'Master of Science, Computer Science',
    school: 'University of Minnesota-Twin Cities',
    gpa: '3.9 GPA',
    years: 'Sep 2023 – Dec 2025',
    details: [
      'Graduate coursework in advanced computer science topics.',
    ],
    logo: '/umn.svg',
  },
  {
    degree: 'Bachelor of Science, Computer Science; Mathematics Minor',
    school: 'University of Minnesota-Twin Cities',
    gpa: '3.7 GPA',
    years: 'Sep 2020 – Dec 2024',
    details: [
      'Undergraduate coursework in computer science and mathematics.',
    ],
    logo: '/umn.svg',
  },
];

const workData = [
  {
    position: 'Software Engineer Intern',
    company: 'Headway',
    years: 'May 2025 – Aug 2025',
    details: [
      'Developed frontend features using React and Remix, contributing to a seamless and responsive user experience.',
      'Designed and built the rebooking flow, enabling patients to easily schedule follow-up appointments with previously seen providers.',
      'Collaborated cross-functionally with product and design teams to ensure user-centric development and adherence to business requirements.',
    ],
    logo: '/headway.svg',
  },
  {
    position: 'Software Engineer Intern',
    company: 'Walmart Global Tech',
    years: 'Jun 2024 – Aug 2024',
    details: [
      'Automated business process to add substitutes for items in internal merchandising tool using Java Spring, generating 500+ new subs biweekly, preventing ~$5000 in lost GMV per week.',
      'Analyzed customer transaction history data with Google BigQuery and Python to identify items that have few high-success substitutes if they were unavailable after being ordered.',
      'Algorithmically mapped items to suitable substitutes with over 80% customer acceptance rate using item attributes and data in Google Cloud Platform, Druid, and Postgres databases.',
      'Created an ETL pipeline to move and process data to support sub automation using Python and ApacheSpark.',
      'Tracked performance of subs using Looker Studio and Python.',
    ],
    logo: '/walmart.svg',
  },
  {
    position: 'Undergraduate Researcher',
    company: 'University of Minnesota-Twin Cities',
    years: 'Sep 2023 – Dec 2023',
    details: [
      'Designed and developed a debugger for Silver, an extensible attribute grammar specification language used to develop UMN\'s extensible implementation of C, AbleC.',
      'Learned extensively about functional programming and stateless programming languages like OCaml.',
    ],
    logo: '/umn.svg',
  },
  {
    position: 'Software Engineer',
    company: 'Other World Computing',
    years: 'Oct 2022 – Oct 2023',
    details: [
      'Built a RESTful API to import sales orders from eCommerce site to Dynamics 365, supporting up to 5,000 orders daily.',
      'Led development of extensions for RMA app support and Salesforce Integration for Dynamics 365.',
      'Maintained applications built with .NET Framework/C#, JavaScript, and PHP.',
      'Created reports for marketing and warehouse teams within Dynamics 365.',
      'Developed and performed administrative duties within Salesforce to reduce data duplication and spam.',
    ],
    logo: 'owc.svg',
  },
];

export default function About() {
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState<any>(null);
  const [modalType, setModalType] = useState<'education' | 'work' | null>(null);

  const handleCardClick = (data: any, type: 'education' | 'work') => {
    setModalData(data);
    setModalType(type);
    setModalOpen(true);
  };

  const handleClose = () => {
    setModalOpen(false);
    setModalData(null);
    setModalType(null);
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8 text-center">About Me</h1>

      {/* Education Section */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Education</h2>
        <ul className="space-y-6">
          {educationData.map((edu, idx) => (
            <li key={idx}>
              <EducationCard
                onClick={() => handleCardClick(edu, 'education')}
                logo={edu.logo}
                degree={edu.degree}
                school={edu.school}
              />
            </li>
          ))}
        </ul>
      </section>

      {/* Work Experience Section */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Work Experience</h2>
        <ul className="space-y-6">
          {workData.map((work, idx) => (
            <li key={idx}>
              <WorkCard
                onClick={() => handleCardClick(work, 'work')}
                logo={work.logo}
                position={work.position}
                company={work.company}
              />
            </li>
          ))}
        </ul>
      </section>

      {/* Modal for more info */}
      <InfoModal
        open={modalOpen}
        onClose={handleClose}
        modalData={modalData}
        modalType={modalType}
      />
    </div>
  );
}

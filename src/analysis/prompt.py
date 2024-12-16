class Prompt:
    balance_sheet = """ 
        {balance_sheet}
        
        Analyze the balance sheet of this real estate company to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    income_statement = """
        {income_statement}

        Analyze the income statement of this real estate company to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    revenue = """
        {revenue_detailed}

        Analyze the revenue details of this real estate company to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    labor = """
        {labor}

        Analyze the labor data of this real estate company to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    is_month_comparative = """
        This is the company top 10 percentage variance:
        {percent_var_top}
        
        This is the company top 10 dollar variance:
        {dollar_var_top}

        Analyze the finance variance data of this real estate company to assess its financial health and performance. Identify key financial ratios and trends to provide a comprehensive overview of its financial position. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """

    master = """
        Given these analysis of these financial data of a real estate company, compile a complete analysis of what is going on, what should decision maker be aware of and what is the potential course of action. Your analysis should be as concise as possible without compromising any information and do not make up numbers and things.
    """
